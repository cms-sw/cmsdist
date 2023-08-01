### RPM cms t0wmadatasvc 2.0.0
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define webdoc_files %{installroot}/%{pkgrel}/doc/
%define wmcver 2.1.4

Source0: git+https://github.com/dmwm/WMCore?obj=master/%wmcver&export=wmcore_%n&output=/wmcore_%n.tar.gz
Source1: git+https://github.com/germanfgv/t0wmadatasvc?obj=master/%realversion&export=%n&output=/%n.tar.gz

Requires: py3-cherrypy py3-cx-oracle py3-pycurl py3-future rotatelogs
BuildRequires: wmcorepy3-devtools

%prep
%setup -T -b 0 -n wmcore_%n
%setup -D -T -b 1 -n %n
perl -p -i -e "s{<VERSION>}{%{realversion}}g" doc/conf.py

echo "BUILDING T0WMADATASVC"
%build
cd ../wmcore_%n
python3 setup.py build_system -s wmc-rest --skip-docs
PYTHONPATH=$PWD/build/lib:$PYTHONPATH
cd ../%n
python3 setup.py build_system --skip-docs

echo "INSTALLING T0WMADATASVC"
%install
mkdir -p %i/etc/profile.d %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
cd ../wmcore_%n
python3 setup.py install_system -s wmc-rest --prefix=%i
perl -p -i -e 's/WMCORE_ROOT/T0WMADATASVC_ROOT/g' %i/bin/wmc-*
# Hack to remove this unneeded check. Should instead fix this directly in WMCore.
perl -p -i -e 's,\[ -x bin/wmc-dist-patch.*,,g' %i/bin/wmc-dist-patch 

cd ../%n
python3 setup.py install_system --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python3}'

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/{env,dep*}.*sh

%files
%{installroot}/%{pkgrel}/
%exclude %{installroot}/%{pkgrel}/doc

## SUBPACKAGE webdoc
