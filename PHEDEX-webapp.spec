pre27PM cms PHEDEX-webapp WEBAPP_BETA_1_0_0pre27
# note: trailing letters in version are ignored when fetching from cvs
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|WEBAPP_||' | sed 's|_|.|g')
%define cvsversion %(echo %v | sed 's/[a-z]$//')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source: %cvsserver&strategy=checkout&module=%{downloadn}&export=%{downloadn}&&tag=-r%{cvsversion}&output=/%{n}.tar.gz
# Would love to 'require' the PHEDEX_datasvc, but I don't see how I can do that
# the post-install for the datasvc requires a trim-cache job, but I cannot
# include that in the RPM, so it has to be 'Deploy'ed separately. Yuck!
#Requires: protovis yui PHEDEX-datasvc
Requires: protovis yui

# We obsolete each previous release to force them to be removed
# Prior to BETA_0_9, WEBAPP was known as APPSERV
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_8
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_7
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_5
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_4
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_2
Obsoletes: cms+PHEDEX-appserv+APPSERV_BETA_0_1

%prep
%setup -n PHEDEX

%build
echo 'now in the build section'
pwd
cd %_builddir
sh %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/util/phedex-minify.sh
rm -rf %_builddir/PHEDEX/PhEDExWeb/{ApplicationServer/{js,css,util},yuicompressor*}
mv %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/{build/*,}
rmdir %_builddir/PHEDEX/PhEDExWeb/ApplicationServer/build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)
echo 'manifest of installation'
find %i -type f

rm -f %instroot/apache2/apps.d/webapp-httpd.conf

# Set template variables in deployment files
export DOCUMENT_ROOT=%i/PhEDExWeb/ApplicationServer
export VERSION=%nversion
export PROJECT_ROOT='%instroot/../projects/phedex-webapp'
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -p -i -e "
  s|\@SERVER_ROOT\@|%instroot/apache2|g;
  s|\@PROJECT_ROOT\@|$PROJECT_ROOT|g;
  s|\@DOCUMENT_ROOT\@|$DOCUMENT_ROOT|g;
  s|\@YUI_ROOT\@|$YUI_ROOT|g; \
  s|\@PROTOVIS_ROOT\@|$PROTOVIS_ROOT|g;" \
  %i/PhEDExWeb/ApplicationServer/conf/webapp-httpd.conf

export WEBAPP_BASEURL='/phedex/datasvc/app'
export WEBAPP_DATASERVICEURL='/phedex/datasvc/json/'
perl -p -i -e "s|\@WEBAPP_VERSION\@|$VERSION|g; \
               s|\@WEBAPP_BASEURL\@|$WEBAPP_BASEURL|g; \
               s|\@WEBAPP_DATASERVICEURL\@|$WEBAPP_DATASERVICEURL|g;" \
  %i/PhEDExWeb/ApplicationServer/js/phedex-base{,-loader}{,-min}.js
cp %i/PhEDExWeb/ApplicationServer/html/phedex{,-debug}.html
# Replace the base and loader files with the rollup, and switch everything to minified files.
# Also explicitly turn off combo-serving, for now.
perl -p -i -e 's|phedex-base.js|phedex-base-loader.js|; \
	      s|^.*phedex-loader.js.*||; \
	      s|phedex([a-z,-]+).js|phedex\1-min.js|g; \
	      s|PHEDEX.Appserv.combineRequests.*$|PHEDEX.Appserv.combineRequests = false;|g;' \
  %i/PhEDExWeb/ApplicationServer/html/phedex.html

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
SERVER_CONF=$RPM_INSTALL_PREFIX/apache2/apps.d
INSTALL_CONF=PhEDExWeb/ApplicationServer/conf
FULL_INSTALL_CONF=$RPM_INSTALL_PREFIX/%{pkgrel}/$INSTALL_CONF
%{relocateConfig}$INSTALL_CONF/webapp-httpd.conf

# Clean out any old appserv config file(s)
if [ -f $RPM_INSTALL_PREFIX/apache2/apps.d/datasvc-xappserv.conf ]; then
  rm $RPM_INSTALL_PREFIX/apache2/apps.d/datasvc-xappserv.conf
fi

# copy to apps.d/ directory.
cp -p $FULL_INSTALL_CONF/webapp-httpd.conf $SERVER_CONF/webapp-httpd.conf

%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

%files
%i/
# does not work.  
#%instroot/apache2/apps.d/datasvc-httpd.conf.02-webapp
#%attr(444,-,-) %config %instroot/apache2/apps.d/datasvc-httpd.conf.02-webapp
