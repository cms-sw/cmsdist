### RPM external py2-future 0.15.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/f/future/future-%realversion.tar.gz
Requires: python py2-setuptools py2-importlib py2-argparse

%prep
%setup -n future-%realversion

%build
python setup.py build

%install
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null

# Don't delete egg-info since the futurize script need it to load the future library
#find %i -name '*.egg-info' -print0 | xargs -0 rm -rf --

# Fix hardcoded path to python
egrep -r -l '^#!.*python' %i/bin | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
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
