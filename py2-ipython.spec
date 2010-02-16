### RPM external py2-ipython 0.10
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://ipython.scipy.org/dist/%realversion/ipython-%realversion.tar.gz
Requires: python

%prep
%setup -n ipython-%realversion

%build

%install
mkdir -p %i/bin
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
python setup.py install --prefix=%i
cd %i/bin
for name in `ls`;
do
    cat $name | sed -e "s,#\!/.*python$,#\!/usr/bin/env python,g" > $name.tmp
    rm -f $name
    mv $name.tmp $name
    chmod a+x $name
done

#mv build/lib*/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
#cp build/script*/* %i/bin/

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
