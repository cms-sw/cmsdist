### RPM external py2-scikit-learn 0.16.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
Source: https://pypi.python.org/packages/source/s/scikit-learn/scikit-learn-%realversion.tar.gz
Requires: python py2-numpy py2-scipy py2-matplotlib

%prep
%setup -n scikit-learn-%realversion

%build
%install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

mkdir -p %i/$PYTHON_LIB_SITE_PACKAGES
PYTHONPATH=%i/$PYTHON_LIB_SITE_PACKAGES:$PYTHONPATH \
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
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
