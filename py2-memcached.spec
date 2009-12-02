### RPM external py2-memcached 1.43
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

# The first line above define location of our RPM in CMS RPM repositoy (external), the RPM name
# (py2-memcached) and RPM version of the package (1.43). The we define local variable
# pythonv and use CMS macro INITENV to define initial path and python path.
# Below we define set of instruction for RPM build system to build our package.

# define location of the memcached code. Here realversion defines version of the package we will 
# retrieve from specified location (can be http/ftp/cvs). 
# The realversion is defined by first line in this file, py2-memcached 1.43, first it's a new
# name for our RPM and 1.43 is RPM package version (realversion).
Source: ftp://ftp.tummy.com/pub/python-memcached/old-releases/python-memcached-%realversion.tar.gz

# define dependencies for memcached
Requires: python py2-setuptools memcached

# pre-build step, put your instruction here, e.g. define environment
# here we use %setup instruction to setup package directory where package will be located.
# the name, python-memcached-1.43 is what we get when untar the tarball, so we put here
# python-memcached-%realversion
%prep 
%setup -n python-memcached-%realversion

# put here build instruction, e.g. make build, since python code doesn't require
# any special instruction we leave this section blank
%build

# install instructions, e.g. make install, in our case we can use just
# python setup.py build to build and package and move build code into install area
# Here %i refers to install area where our package will be installed
%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
mv build/lib/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages


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
