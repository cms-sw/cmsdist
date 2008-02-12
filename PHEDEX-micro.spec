### RPM cms PHEDEX-micro PHEDEX_2_6_0
#####
## INITENV +PATH PATH %i/Utilities:%i/Toolkit/DBS:%i/Toolkit/DropBox:%i/Toolkit/Request
## INITENV +PATH PERL5LIB %i/perl_lib
%define downloadn %(echo %n | cut -f1 -d-)
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{downloadn}.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser python
Requires: p5-monalisa-apmon

# Provided by system perl
Provides: perl(HTML::Entities)

%prep
%setup -n %{downloadn}
rm     Custom/Template/Config
rm     Custom/Template/ConfigPart.CERN*
rm     Custom/Template/ConfigPart.Export
rm     Custom/Template/ConfigPart.FTSDownload
rm     Custom/Template/ConfigPart.Management
rm     Custom/Template/ConfigPart.MSS
rm     Custom/Template/ConfigPart.SRMDownload
rm     Custom/Template/File*
rm     Custom/Template/ProxyRenew
rm     Custom/Template/storage.xml
rm -rf Custom/DCache
rm -rf Custom/Castor
rm -rf Custom/SRM
rm -rf Schema
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Monitoring
rm -rf Toolkit/Transfer
rm -rf Toolkit/Workflow
find Utilities -type f | egrep -v "OracleConnectId|Master" | xargs rm

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
