### RPM cms PHEDEX-datasvc DATASVC_1_2_1
#
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|DATASVC_||' | sed 's|_|.|g')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

Source: %cvsserver&strategy=checkout&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{n}.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser
Requires: p5-cgi p5-json-xs p5-apache-dbi
Requires: apache2-conf mod_perl2 webtools

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)

# We obsolete each previous release to force them to be removed
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_2_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_1_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_0_0

%prep
%setup -n PHEDEX

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

rm -f %instroot/apache2/startenv.d/datasvc-env.sh
rm -f %instroot/apache2/apps.d/datasvc-httpd.conf

# Switch template variables in the configuration files
export DOCUMENT_ROOT=%i/PhEDExWeb/DataService
export CACHE_DIRECTORY=/tmp/phedex-datasvc
export VERSION=%nversion
perl -p -i -e "s|\@DOCUMENT_ROOT\@|$DOCUMENT_ROOT|g;
	       s|\@SERVER_ROOT\@|%instroot/apache2|g;
	       s|\@CACHE_DIRECTORY\@|$CACHE_DIRECTORY|g;
               s|\@VERSION\@|$VERSION|g;
	       s|\@MOD_PERL_LIB\@|$MOD_PERL2_ROOT/modules/mod_perl.so|g;" \
  %i/PhEDExWeb/DataService/conf/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
mkdir -p /tmp/phedex-datasvc
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-app.conf
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-httpd.conf
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-secmod.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

# Copy files to apache2 directory
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-httpd.conf $RPM_INSTALL_PREFIX/apache2/apps.d
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh $RPM_INSTALL_PREFIX/apache2/startenv.d/datasvc-env.sh

%files
%i/
# %files processed before %post? listing these files causes a build failure
# %attr(444,-,-) %config %instroot/apache2/apps.d/datasvc-httpd.conf
# %attr(444,-,-) %config %instroot/apache2/startenv.d/datasvc-env.sh
