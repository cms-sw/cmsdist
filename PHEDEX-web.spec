### RPM cms PHEDEX-web WEB_3_1_3
# note: trailing letters in version are ignored when fetching from cvs
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|WEB_||' | sed 's|_|.|g')
%define cvsversion %(echo %v | sed 's/[a-z]$//')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define deployutil WTDeployUtil.pm
%define deployutilrev 1.5
%define deployutilurl http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/COMP/WEBTOOLS/Configuration/%{deployutil}?revision=%{deployutilrev}

Source: %cvsserver&strategy=checkout&module=%{downloadn}&export=%{downloadn}&&tag=-r%{cvsversion}&output=/%{n}.tar.gz

# For DB Access
Requires: oracle oracle-env p5-dbi p5-dbd-oracle
# Core for web apps
Requires: apache2-conf mod_perl2 p5-apache-dbi webtools p5-cgi p5-cgi-session
# Useful for web apps
Requires: p5-json-xs p5-xml-parser
# Misc. Utilities
Requires: p5-params-validate p5-clone p5-time-hires p5-text-glob p5-compress-zlib p5-sort-key p5-mail-rfc822-address
Requires: p5-log-log4perl
# For GraphTool component
Requires: py2-pil py2-matplotlib py2-numpy libjpg py2-pytz

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(XML::LibXML)

# We obsolete each previous release to force them to be removed
Obsoletes: cms+PHEDEX-web+WEB_3_1_2a
Obsoletes: cms+PHEDEX-web+WEB_3_1_2
Obsoletes: cms+PHEDEX-web+WEB_3_1_1b
Obsoletes: cms+PHEDEX-web+WEB_3_1_1a
Obsoletes: cms+PHEDEX-web+WEB_3_1_1
Obsoletes: cms+PHEDEX-web+WEB_3_1_0
Obsoletes: cms+PHEDEX-web+WEB_3_0_2
Obsoletes: cms+PHEDEX-web+WEB_3_0_1
Obsoletes: cms+PHEDEX-web+WEB_3_0_0

%prep
%setup -n PHEDEX
wget -O %{deployutil} '%{deployutilurl}'

%build
%install
tar -cf - * | (cd %i && tar -xf -)

rm -f %instroot/apache2/etc/startenv.d/phedexweb-env.sh
rm -f %instroot/apache2/apps.d/phedexweb-httpd.conf

# Switch path-like template variables in the configuration files
perl -p -i -e "s|\@PHEDEX_ROOT\@|%i|g;
	       s|\@SERVER_ROOT\@|%instroot/apache2|g;
	       s|\@MOD_PERL_LIB\@|$MOD_PERL2_ROOT/modules/mod_perl.so|g;" \
  %i/Documentation/WebConfig/* \
  %i/Documentation/WebSite/PlotConfig/config/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# cp startup scripts to /bin
mkdir -p %i/bin
cp %i/Documentation/WebConfig/cmsweb_phedex_graphs %i/bin

%post
# Relocate the package

%{relocateConfig}Documentation/WebConfig/phedexweb-httpd.conf
%{relocateConfig}Documentation/WebConfig/phedexweb-app.conf
%{relocateConfig}Documentation/WebConfig/phedexweb-secmod.conf
%{relocateConfig}Documentation/WebSite/PlotConfig/config/cherrypy_prod.conf
%{relocateConfig}bin/cmsweb_phedex_graphs
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# Switch host-like template variables in the configuration files
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -e '
  print "Configuring service for @{[&WTDeployUtil::deployment()]} on @{[&WTDeployUtil::my_host()]}\n";
'

perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  $hosts = join(" ", &WTDeployUtil::frontend_hosts());
  s|\@FRONTEND_HOSTS\@|$hosts|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/Documentation/WebConfig/phedexweb-httpd.conf

# password file default location
export PHEDEX_DBPARAM=/data/projects/conf/phedex/DBParam
if [ ! -f $PHEDEX_DBPARAM ]; then
  export PHEDEX_DBPARAM=/where/i/put/my/DBParam
fi

perl -p -i -e '
  s|\@PHEDEX_DBPARAM\@|$ENV{PHEDEX_DBPARAM}|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/bin/cmsweb_phedex_graphs

perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  $hosts = join(",", &WTDeployUtil::frontend_ips());
  $alias = &WTDeployUtil::frontend_alias();
  s|\@FRONTEND_IPS\@|$hosts|g;
  s|\@FRONTEND_ALIAS\@|$alias|g;
  s|\@PHEDEX_DBPARAM\@|$ENV{PHEDEX_DBPARAM}|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/Documentation/WebConfig/phedexweb-app.conf

# Copy files to apache2 directory
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/Documentation/WebConfig/phedexweb-httpd.conf $RPM_INSTALL_PREFIX/apache2/apps.d
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/phedexweb-env.sh

# soft link httpd startup script to our bin/
ln -s $RPM_INSTALL_PREFIX/apache2/etc/init.d/httpd $RPM_INSTALL_PREFIX/%{pkgrel}/bin/httpd

# Relocate those files
#perl -p -i -e "s|%instroot|$RPM_INSTALL_PREFIX|g" \ 
# $RPM_INSTALL_PREFIX/apache2/apps.d/phedexweb-httpd.conf \
# $RPM_INSTALL_PREFIX/apache2/startenv.d/phedexweb-env.sh
 
%files
%i/
# %files processed before %post? listing these files causes a build failure
# %attr(444,-,-) %config %instroot/apache2/apps.d/phedexweb-httpd.conf
# %attr(444,-,-) %config %instroot/apache2/startenv.d/phedexweb-env.sh
