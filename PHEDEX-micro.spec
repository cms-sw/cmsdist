### RPM cms PHEDEX-micro PHEDEX_2_5_3_5
##
## INITENV +PATH PATH %i/Utilities:%i/Toolkit/DBS:%i/Toolkit/DropBox:%i/Toolkit/Request
%define downloadn %(echo %n | cut -f1 -d-)
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%{downloadn}&export=%{downloadn}&&tag=-r%{v}&output=/%{downloadn}.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser srmcp python
Requires: py2-cx-oracle

# Extra requires so we get everything necessary for env.{,c}sh.
Requires: zlib expat openssl bz2lib py2-pyxml py2-zsi py2-mysqldb mysql

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
rm -rf Deployment
rm -rf Schema
rm -rf Testbed
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Management
rm -rf Toolkit/Monitoring
rm -rf Toolkit/Peers
rm     Toolkit/Request/TR*
rm -rf Toolkit/Test
rm -rf Toolkit/Transfer
rm -rf Toolkit/Workflow
rm     Utilities/CMSSWMigrate
rm     Utilities/DBDump
rm     Utilities/DBLoad
rm     Utilities/DBSCheck
rm     Utilities/DropStatus
rm     Utilities/DSBFill
rm     Utilities/FileDeleteTMDB
rm     Utilities/ftscp
rm     Utilities/GetLocalPath
rm     Utilities/GrepSites
rm     Utilities/InspectPhedexLog
rm     Utilities/LinkNew
rm     Utilities/LinkRemove
rm     Utilities/LoadTest07FileCreator
rm     Utilities/MakeDailyReport
rm     Utilities/MakeDailyStats
rm     Utilities/netmon
rm     Utilities/NodeNew
rm     Utilities/NodeRemove
rm     Utilities/RunTest
rm     Utilities/TestCatalogue
rm     Utilities/UtilGraphTopology
rm     Utilities/WordMunger

%build

%install
mkdir -p %i/etc
tar -cf - * | (cd %i && tar -xf -)

mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 case $x in *gcc* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/env.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/env.csh
done
cat %i/etc/profile.d/env.csh > %i/etc/profile.d/dependencies-setup.csh
cat %i/etc/profile.d/env.sh > %i/etc/profile.d/dependencies-setup.sh
%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
