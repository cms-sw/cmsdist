### RPM external mongo 1.4.0
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages 
## INITENV +PATH PYTHONPATH $SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages
## INITENV +PATH PYTHONPATH $SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/scons
## INITENV +PATH PYTHONPATH $SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/scons/Scons

Provides: libpcap.so.0.8.3
# 64-bit versions
Provides: libpcap.so.0.8.3()(64bit)
Source: http://downloads.mongodb.org/src/mongodb-src-r%{realversion}.tar.gz
Requires: gcc boost scons pcre spidermonkey
#Patch1: mongo.scons

%prep
#%setup -n mongo
%setup -n mongodb-src-r%{realversion}
#%patch1 -p0

%build
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/:$PYTHONPATH
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/SCons/:$PYTHONPATH
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/SCons/Tool:$PYTHONPATH
export PATH=$PATH:$SCONS_ROOT/bin
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT all

%install
#cp -r bin include lib %{i}/
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/:$PYTHONPATH
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/SCons/:$PYTHONPATH
export PYTHONPATH=$SCONS_ROOT/lib/python`echo $PYTHON_VERSION | cut -d. -f1,2`/site-packages/SCons/Tool:$PYTHONPATH
export PATH=$PATH:$SCONS_ROOT/bin
export CXX=$GCC_ROOT/bin/g++
#scons --64 --cxx=$CXX --extrapath=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install
scons --64 --cxx=$CXX --extrapathdyn=$PCRE_ROOT,$BOOST_ROOT,$SPIDERMONKEY_ROOT --prefix=%i install

mkdir -p %i/etc/profile.d/
# This will generate the correct dependencies-setup.sh/dependencies-setup.csh
# using the information found in the Requires statements of the different
# specs and their dependencies.
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
