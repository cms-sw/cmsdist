### RPM cms PHEDEX-datasvc DATASVC_1_6_4pre6
# note: trailing letters in version are ignored when fetching from cvs
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|DATASVC_||' | sed 's|_|.|g')
%define cvsversion %(echo %v | sed 's/[a-z]$//')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e

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

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)

# We obsolete each previous release to force them to be removed
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_6_3
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_6_2
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_6_1
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_6_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_5_2
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_5_1
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_5_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_4_2a
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_4_2
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_4_1
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_4_0a
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_4_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_3_1b
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_3_1a
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_3_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_2_1
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_2_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_1_0
Obsoletes: cms+PHEDEX-datasvc+DATASVC_1_0_0

%prep
%setup -n PHEDEX

%build
%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

rm -f %instroot/apache2/etc/startenv.d/datasvc-env.sh
rm -f %instroot/apache2/apps.d/datasvc-httpd.conf

# Switch path-link template variables in the configuration files
export DOCUMENT_ROOT=%i/PhEDExWeb/DataService
export VERSION=%nversion
export PROJECT_ROOT='%instroot/../projects/phedex-webapp'
export CACHE_DIRECTORY=$PROJECT_ROOT/cache/phedex-datasvc
perl -p -i -e "s|\@DOCUMENT_ROOT\@|$DOCUMENT_ROOT|g;
	       s|\@SERVER_ROOT\@|%instroot/apache2|g;
	       s|\@PROJECT_ROOT\@|$PROJECT_ROOT|g;
	       s|\@CACHE_DIRECTORY\@|$CACHE_DIRECTORY|g;
               s|\@VERSION\@|$VERSION|g;
	       s|\@MOD_PERL_LIB\@|$MOD_PERL2_ROOT/modules/mod_perl.so|g;
	       s|\@APACHE2_MODULES\@|$APACHE2_ROOT/modules|g;" \
  %i/PhEDExWeb/DataService/conf/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Make a script to clean the cache
mkdir -p %i/bin
echo "#!/bin/bash
source %i/etc/profile.d/init.sh
htcacheclean -n -t -p $CACHE_DIRECTORY -l \$1
" > %i/bin/trim-cache
chmod 544 %i/bin/trim-cache

%post
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-app.conf
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-httpd.conf
%{relocateConfig}PhEDExWeb/DataService/conf/datasvc-secmod.conf
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}bin/trim-cache

# password file default location
export PHEDEX_DBPARAM=/data/projects/conf/phedex/DBParam
if [ ! -f $PHEDEX_DBPARAM ]; then
  export PHEDEX_DBPARAM=/where/i/put/my/DBParam
fi
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -p -i -e '
  s|\@PHEDEX_DBPARAM\@|$ENV{PHEDEX_DBPARAM}|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-app.conf

# Copy files to apache2 directory
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-httpd.conf $RPM_INSTALL_PREFIX/apache2/apps.d
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/datasvc-env.sh

%files
%i/
# %files processed before %post? listing these files causes a build failure
# %attr(444,-,-) %config %instroot/apache2/apps.d/datasvc-httpd.conf
# %attr(444,-,-) %config %instroot/apache2/etc/startenv.d/datasvc-env.sh
