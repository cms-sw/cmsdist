### RPM cms PHEDEX-micro PHEDEX_4_1_3pre1

## INITENV +PATH PATH %i/Utilities:%i/Toolkit/DBS:%i/Toolkit/DropBox:%i/Toolkit/Request
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
Source: git://github.com/dmwm/PHEDEX?obj=master/788560654b78555c96b71aa66c99e59e2b30581d&export=%n&output=/%{downloadn}-micro.tar.gz

# Oracle libs
Requires: oracle oracle-env
# perl libs
Requires: p5-time-hires p5-text-glob p5-compress-zlib p5-dbi
Requires: p5-dbd-oracle p5-xml-parser p5-poe p5-poe-component-child
Requires: p5-log-log4perl p5-log-dispatch p5-log-dispatch-filerotate
Requires: p5-params-validate p5-monalisa-apmon
# CMS COMP clients
Requires: dbs-client
# Etc.
Requires: python
# Actually, it is p5-xml-parser that requires this, but it doesn't configure itself correctly
# This is so it gets into our dependencies-setup.sh
Requires: expat

# Provided by system perl
Provides: perl(HTML::Entities)
Provides: perl(DB_File)
Provides: perl(Date::Manip)
Provides: perl(XML::LibXML)

# Fake provide of twitter client; needs to be installed manually
Provides: perl(Net::Twitter::Lite)

%prep

%setup -n %{downloadn}-micro
rm -rf Custom/Template/*
rm -rf Custom/DCache
rm -rf Custom/Castor
rm -rf Custom/SRM
rm -rf Schema
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Monitoring
rm -rf Toolkit/Transfer
rm -rf Toolkit/Workflow
rm -rf Toolkit/Verify
rm -rf Toolkit/DropBox
rm -rf Utilities/AgentFactory.pl
rm -rf Utilities/AgentMon.pl                                                
rm -rf Utilities/CMSSWMigrate
rm -rf Utilities/DBDump
rm -rf Utilities/DBLoad
rm -rf Utilities/DropStatus
rm -rf Utilities/FillNames
rm -rf Utilities/GrepSites
rm -rf Utilities/ping-watchdog.pl
rm -rf Utilities/stagercp
rm -rf Utilities/WordMunger
rm -rf Utilities/wrapper_rfcp

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

# Set permissions
chmod 755 %i/Toolkit/DBS/*
chmod 755 %i/Utilities/*

# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

# Make "env.sh" = "init.sh" for legacy configs
echo ". %i/etc/profile.d/init.sh" > %i/etc/profile.d/env.sh
echo "source %i/etc/profile.d/init.csh" > %i/etc/profile.d/env.csh

%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
