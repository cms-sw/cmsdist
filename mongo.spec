### RPM external mongo 3.0.7
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: http://downloads.mongodb.org/src/mongodb-src-r%{realversion}.tar.gz
Requires: python scons rotatelogs
BuildRequires: gcc

Provides: libpcap.so.0.8.3
Provides: libpcap.so.0.8.3()(64bit)

%prep
%setup -n mongodb-src-r%{realversion}
perl -p -i -e 's/-rdynamic//' SConstruct
perl -p -i -e 's/"-mt"/""/' SConstruct
# get rid of /usr/bin/python
egrep -r -l '^#!.*python' . | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'

%build

%install
# make wrappers for scons
mkdir -p $PWD/bin
cat > g++-wrapper << EOF
#!/bin/bash
source $GCC_ROOT/etc/profile.d/init.sh
\$GCC_ROOT/bin/g++ \$@
EOF
chmod +x g++-wrapper
cat > gcc-wrapper << EOF
#!/bin/bash
source $GCC_ROOT/etc/profile.d/init.sh
\$GCC_ROOT/bin/gcc \$@
EOF
chmod +x gcc-wrapper

case "%{cmsplatf}" in osx*) X64= ;; *) X64=--64 ;; esac
# we need to expose LD_LIBRARY_PATH into scons environment
# since it calls our python and python should find its libs
scons %makeprocesses $X64 --propagate-shell-environment=LD_LIBRARY_PATH --cxx=./g++-wrapper --cc=./gcc-wrapper --prefix=%i install

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
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
