### RPM cms PHEDEX-datasvc DATASVC_1_5_1
#
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
%define nversion %(echo %v | sed 's|DATASVC_||' | sed 's|_|.|g')
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
%define deployutil WTDeployUtil.pm
%define deployutilrev 1.5
%define deployutilurl http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/COMP/WEBTOOLS/Configuration/%{deployutil}?revision=%{deployutilrev}

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
wget -O %{deployutil} '%{deployutilurl}'

%build
%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

rm -f %instroot/apache2/etc/startenv.d/datasvc-env.sh
rm -f %instroot/apache2/apps.d/datasvc-httpd.conf

# Switch path-link template variables in the configuration files
export DOCUMENT_ROOT=%i/PhEDExWeb/DataService
export CACHE_DIRECTORY=%instroot/apache2/var/cache/phedex-datasvc
export VERSION=%nversion
perl -p -i -e "s|\@DOCUMENT_ROOT\@|$DOCUMENT_ROOT|g;
	       s|\@SERVER_ROOT\@|%instroot/apache2|g;
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

# Switch host-like template variables in the configuration files
perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -e '
  print "Configuring service for @{[&WTDeployUtil::deployment()]} on @{[&WTDeployUtil::my_host()]}\n";
'

perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  $hosts = join(" ", &WTDeployUtil::frontend_hosts());
  s|\@FRONTEND_HOSTS\@|$hosts|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-httpd.conf

# password file default location
export PHEDEX_DBPARAM=/data/projects/conf/phedex/DBParam
if [ ! -f $PHEDEX_DBPARAM ]; then
  export PHEDEX_DBPARAM=/where/i/put/my/DBParam
fi

perl -I  $RPM_INSTALL_PREFIX/%{pkgrel} -MWTDeployUtil -p -i -e '
  $hosts = join(",", &WTDeployUtil::frontend_ips());
  $alias = &WTDeployUtil::frontend_alias();
  s|\@FRONTEND_IPS\@|$hosts|g;
  s|\@FRONTEND_ALIAS\@|$alias|g;
  s|\@PHEDEX_DBPARAM\@|$ENV{PHEDEX_DBPARAM}|g;
'  $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-app.conf


# Copy files to apache2 directory
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/PhEDExWeb/DataService/conf/datasvc-httpd.conf $RPM_INSTALL_PREFIX/apache2/apps.d
cp -p $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh $RPM_INSTALL_PREFIX/apache2/etc/startenv.d/datasvc-env.sh

# Create cache directory
mkdir -p $RPM_INSTALL_PREFIX/apache2/var/cache/phedex-datasvc

%files
%i/
# %files processed before %post? listing these files causes a build failure
# %attr(444,-,-) %config %instroot/apache2/apps.d/datasvc-httpd.conf
# %attr(444,-,-) %config %instroot/apache2/etc/startenv.d/datasvc-env.sh
