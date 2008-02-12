### RPM cms PHEDEX PHEDEX_2_6_0
####
## INITENV +PATH PERL5LIB %i/perl_lib
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%n&export=%n&&tag=-r%{v}&output=/%n.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser python
Requires: dbs-client p5-monalisa-apmon

# Provided by system perl
Provides: perl(HTML::Entities)

%prep
%setup -n %n
rm -f  Custom/Template/Config.Micro
rm -f  Custom/Template/ConfigPart.CERN*
rm -f  Custom/Template/ConfigPart.Management
rm -rf Schema
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Monitoring
rm -rf Toolkit/Workflow
rm -f  Utilities/CMSSWMigrate
rm -f  Utilities/DBDump
rm -f  Utilities/DBLoad
rm -f  Utilities/DBSCheck
rm -f  Utilities/GrepSites
rm -f  Utilities/FileDeleteTMDB
rm -f  Utilities/LinkNew
rm -f  Utilities/LinkRemove
rm -f  Utilities/MakeDailyReport
rm -f  Utilities/MakeDailyStats
rm -f  Utilities/netmon
rm -f  Utilities/NodeNew
rm -f  Utilities/NodeRemove
rm -f  Utilities/RunTest
rm -f  Utilities/WordMunger

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

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
