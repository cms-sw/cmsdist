### RPM cms PHEDEX PHEDEX_2_5_1
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%n&export=%n&&tag=-r%{v}&output=/%n.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle p5-xml-parser srmcp python
Requires: py2-cx-oracle
Requires: dls dbs
Requires: PHEDEX
Provides: perl(UtilsMisc)
Provides: perl(ApMon) perl(Date::Manip)
Provides: perl(POE) perl(POE::Component::Client::TCP) perl(POE::Component::Server::TCP)
Provides: perl(POE::Filter::Reference) perl(POE::Queue::Array) perl(POE::Session)
Provides: perl(POE::Wheel::Run)

# Extra requires so we get everything necessary for env.{,c}sh.
Requires: zlib expat openssl bz2lib py2-pyxml py2-zsi py2-mysqldb mysql


%prep
%setup -n %n
rm -rf Custom
rm -rf Deployment
rm -rf Documentation
rm -rf Toolkit/Common
rm -rf Toolkit/DBS
rm -rf Toolkit/DropBox
rm -rf Toolkit/Infrastructure
rm -rf Toolkit/Request
rm -rf Toolkit/Transfer


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
