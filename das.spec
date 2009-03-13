### RPM cms das V01_00_01
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 

%define cvstag %{realversion}
%define cvsserver cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e
Source: %cvsserver&strategy=checkout&module=COMP/DAS&nocache=true&export=DAS&tag=-r%{cvstag}&output=/das.tar.gz
Requires: python cherrypy yui elementtree py2-simplejson py2-memcached couchdb wmcore

%prep
%setup -n DAS
%build

%install
mkdir -p %{i}/bin
mkdir -p %{i}/test
mkdir -p %{i}/src
mkdir -p %{i}/etc/profile.d
mkdir -p %{i}/etc/init.d
#mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
#cp -r src/python/* %i/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
cp -r bin/* %i/bin
cp -r src/* %i/src
cp -r test/* %i/test

# copy init script
cp bin/das_web %{i}/etc/init.d
chmod a+x %{i}/etc/init.d/*

# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
mkdir -p %i/etc/profile.d
echo '#!/bin/sh' > %{i}/etc/profile.d/dependencies-setup.sh
echo '#!/bin/tcsh' > %{i}/etc/profile.d/dependencies-setup.csh
echo requiredtools `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
for tool in `echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'`
do
    case X$tool in
        Xdistcc|Xccache )
        ;;
        * )
            toolcap=`echo $tool | tr a-z- A-Z_`
            eval echo ". $`echo ${toolcap}_ROOT`/etc/profile.d/init.sh" >> %{i}/etc/profile.d/dependencies-setup.sh
            eval echo "source $`echo ${toolcap}_ROOT`/etc/profile.d/init.csh" >> %{i}/etc/profile.d/dependencies-setup.csh
        ;;
    esac
done
perl -p -i -e 's|\. /etc/profile\.d/init\.sh||' %{i}/etc/profile.d/dependencies-setup.sh
perl -p -i -e 's|source /etc/profile\.d/init\.csh||' %{i}/etc/profile.d/dependencies-setup.csh

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
