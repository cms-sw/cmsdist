### RPM cms PHEDEX PHEDEX_2_5_2

Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%n&export=%n&&tag=-r%{v}&output=/%n.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser srmcp python
Requires: py2-cx-oracle
Requires: dbs-client


# Extra requires so we get everything necessary for env.{,c}sh.
Requires: zlib expat openssl bz2lib py2-pyxml py2-zsi py2-mysqldb mysql

%prep
%setup -n %n
rm -f  Custom/Template/Config.Micro
rm -f  Custom/Template/ConfigPart.CERN*
rm -f  Custom/Template/ConfigPart.Management
rm -rf Schema
rm -rf Testbed
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Management
rm -rf Toolkit/Monitoring
rm -rf Toolkit/Peers
rm -rf Toolkit/Test
rm -rf Toolkit/Workflow
rm -f  Utilities/CMSSWMigrate
rm -f  Utilities/DBDump
rm -f  Utilities/DBLoad
rm -f  Utilities/DBSCheck
rm -f  Utilities/DSBFill
rm -f  Utilities/GrepSites
rm -f  Utilities/FileDeleteTMDB
rm -f  Utilities/IdentityNew
rm -f  Utilities/IdentityRemove
rm -f  Utilities/ImportSites
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

mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/env.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/env.csh
done

%post
%{relocateConfig}etc/profile.d/env.sh
%{relocateConfig}etc/profile.d/env.csh
