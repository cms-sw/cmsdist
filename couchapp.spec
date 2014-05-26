### RPM external couchapp 0.7.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://github.com/couchapp/couchapp/tarball/%realversion?output=/%n-%realversion.tgz
Requires: python py2-setuptools py2-restkit

%prep
%setup -n couchapp-couchapp-202bba1

%build
python setup.py build

%install
# Copy files as requested by Simon
cp -rp %_builddir/couchapp-couchapp-*/* %i/
rm -rf %i/{build,debian,contrib,bin}

# Now build/install as normal procedure would do
python setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
for f in %i/bin/couchapp; do perl -p -i -e 's{.*}{#!/usr/bin/env python} if $. == 1 && m{#!.*/bin/python}' $f; done

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

# Look up documentation online.
%define drop_files %i/[LMNRT]* %i/{doc,tests}

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
