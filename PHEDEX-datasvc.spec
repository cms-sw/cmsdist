### RPM cms PHEDEX-datasvc 2.3.21
## INITENV +PATH PERL5LIB %i/perl_lib

%define downloadn %(echo %n | cut -f1 -d-)
%define downloadp %(echo %n | cut -f2 -d- | tr '[a-z]' '[A-Z]')
%define downloadt %(echo %realversion | tr '.' '_')
%define setupdir  %{downloadn}-%{downloadp}_%{downloadt}
Source: https://github.com/dmwm/PHEDEX/archive/%{downloadp}_%{downloadt}.tar.gz

# For DB Access
Requires: oracle oracle-env p5-dbi p5-dbd-oracle
# Core for web apps
Requires: apache-setup mod_perl2 p5-apache-dbi p5-cgi p5-cgi-session
# Useful for web apps
Requires: p5-json-xs p5-xml-parser
# Misc. Utilities
Requires: p5-params-validate p5-clone p5-time-hires p5-text-glob p5-compress-zlib p5-sort-key p5-mail-rfc822-address
Requires: p5-log-log4perl p5-text-unaccent

# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires:  expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)
Provides: perl(URI::Escape)

%prep
%setup -n %{setupdir}
rm -rf Build Custom Documentation Testbed Utilities
rm -rf Contrib Deployment Migration PhEDExWeb/ApplicationServer Schema Toolkit VERSION
rm -rf perl_lib/{DMWMMON,template}
rm -rf perl_lib/PHEDEX/{BlockActivate,BlockDelete,Debug.pm,Monalisa.pm,Testbed,BlockAllocator,BlockLatency,Error,Monitoring,Transfer,BlockArrive,BlockMonitor,File,Namespace,BlockConsistency,CLI,Infrastructure,BlockDeactivate,LoadTest,Schema}
rm perl_lib/PHEDEX/RequestAllocator/Agent.pm
rm -rf perl_lib/PHEDEX/Core/{Agent,Config.pm,Agent.pm,JobManager.pm,RFIO.pm,Command.pm,Help.pm,SQLPLUS.pm,Config}
rm -rf perl_lib/PHEDEX/Web/SQLSpace.pm
rm -rf perl_lib/PHEDEX/Web/API/{Mongo.pm,RequestSetStateFake.pm,StorageInsert.pm,StorageUsage.pm}

%build
%install
mkdir -p %i/etc/{env,profile}.d
tar -cf - * | (cd %i && tar -xf -)
#rm -r %i/PhEDExWeb/DataService/conf

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
ln -sf ../profile.d/init.sh %i/etc/env.d/11-datasvc.sh
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
