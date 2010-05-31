### RPM external zope-interface 3.3.0

## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)

Requires: python
Source: http://www.zope.org/Products/ZopeInterface/3.3.0/zope.interface-3.3.0.tar.gz

%prep
%setup -n zope.interface-3.3.0

%build

%install
python setup.py install --prefix=%i
# Perhaps the following is needed to fix python source headers
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`

rm -rf %i/etc/profile.d
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


#%files
#%i/
