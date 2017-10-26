### RPM external xgboost 0.60
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

%define pkg1 dmlc-core
%define pkg2 rabit
%define ver1 d8d4dccb8bd89af9f57aa19e7523f0b755563ca4
%define ver2 2dd7476ad7e4afe97eb579d39aab226ff74400a6

Source0: https://github.com/dmlc/%n/archive/v%realversion.tar.gz
Source1: https://github.com/dmlc/%pkg1/archive/%ver1.tar.gz
Source2: https://github.com/dmlc/%pkg2/archive/%ver2.tar.gz
Requires: python py2-numpy py2-scipy py2-scikit-learn py2-setuptools lapack

%prep
%setup -D -T -b 1 -n %pkg1-%ver1
%setup -D -T -b 2 -n %pkg2-%ver2
%setup -T -b 0 -n %n-%realversion
mv ../%pkg1-%ver1/* %pkg1/
mv ../%pkg2-%ver2/* %pkg2/

%build
./build.sh

# stuff to build python APIs
export LAPACK_ROOT
export LAPACK=$LAPACK_ROOT/lib/liblapack.$SONAME
export BLAS=$LAPACK_ROOT/lib/libblas.$SONAME

cd python-package
python setup.py build
cd -

%install
mkdir %i/bin
cp xgboost %i/bin

cd python-package
echo "#### BUILD AREA"
ls build
mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
cp -r ../lib/* build/lib/xgboost
cp -r build/lib/* %i/$PYTHON_LIB_SITE_PACKAGES
#PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
#python setup.py install --prefix=%i
#find %i -name '*.egg-info' -exec rm {} \;
find %i/$PYTHON_LIB_SITE_PACKAGES -name '*.py' -exec chmod a-x {} \;
perl -p -i -e 's{^#!.*/python}{#!/usr/bin/env python}' %i/bin/*

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
