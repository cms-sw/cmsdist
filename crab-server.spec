### RPM cms crab-server CRABSERVER_1_1_3
## INITENV +PATH PYTHONPATH %i/lib
#
%define cvstag %v
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=CRAB/CRABSERVER&export=CRAB&&tag=-r%{cvstag}&output=/CRABSERVER.tar.gz
## boost is needed only by SLC5 build
Requires: prodcommon prodagent boost python-ldap
#Requires: prodcommon prodagent
%prep
%setup -n CRAB
%build

echo "PWD=$PWD"
mv CRABSERVER/* .

%install
make PREFIX=%i install
mkdir -p %i/bin
cp bin/* %{i}/bin

# The following is needed only by SLC5 build
###
pushd src/python/CommandManager/server-side
#  make -f Makefile_2.4 PYHOME=$PYTHON_ROOT BOOST_HOME=$BOOST_ROOT all
  make -f Makefile_2.6 PYHOME=$PYTHON_ROOT BOOST_HOME=$BOOST_ROOT all
  cp FrontendLoader_1_1.so %i/lib/CommandManager/
popd
# While the next is neede for SLC4 BUILD
#pushd src/python/CommandManager/server-side
#  cp FrontendLoader.py _FrontendLoader.so %i/lib/CommandManager/
#popd
###
	
# Copy dependencies to dependencies-setup.sh
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
 case $x in /* ) continue ;; esac
 p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/'
)
 echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
 echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
