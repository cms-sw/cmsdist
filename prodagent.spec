### RPM cms prodagent PRODAGENT_0_12_18_CRAB_2
## INITENV +PATH PYTHONPATH %i/lib
## INITENV +PATH PYTHONPATH $WEBTOOLS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/Tools/GraphTool/src
## INITENV +PATH PYTHONPATH $PY2_PIL_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/PIL
#
#The first line of this file you only edit the version name. This name
# is equal to the with which you tagged the release in cvs. Note: if you 
# do not change the tag and already have uploaded the build packages
# nothing will be created as the cms build application checks the repository.

%define cvstag %v
# where the package is located. Normally this does not change
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=PRODAGENT&export=PRODAGENT&&tag=-r%{cvstag}&output=/PRODAGENT.tar.gz
# dependencies. THis can change from time to time. The names correspond with the spec files of the saem name.
Requires: webtools mysql py2-mysqldb dbs-client prodcommon py2-pyxml PHEDEX-micro py2-numpy py2-matplotlib py2-pil py2-pyopenssl wmcore dls-client

%prep
%setup -n PRODAGENT
%build
%install
make PREFIX=%i install
mkdir -p %i/bin
cp bin/prod* %{i}/bin
mkdir -p %i/test
cp -R test/* %i/test/
mkdir -p %i/util
cp -R util/* %i/util/
mkdir -p %i/ops
cp -R ops/* %i/ops/
mkdir -p %i/workdir

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

