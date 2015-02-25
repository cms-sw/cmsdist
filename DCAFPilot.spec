### RPM cms DCAFPilot 0.0.27
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
%define pkg DCAFPilot
Source: git://github.com/dmwm/DMWMAnalytics.git?obj=master/%realversion&export=%pkg&output=/%pkg.tar.gz
Requires: python py2-numpy py2-scipy py2-scikit-learn py2-pymongo
BuildRequires: py2-sphinx

# RPM macros documentation
# http://www.rpm.org/max-rpm/s1-rpm-inside-macros.html
%prep
%setup -b 0 -n %pkg

%build
cd Popularity/DCAFPilot
python setup.py build

# build sphinx documentation
cd doc
mkdir -p sphinx/_static
cat sphinx/conf.py | sed "s,development,%{realversion},g" > sphinx/conf.py.tmp
mv sphinx/conf.py.tmp sphinx/conf.py
mkdir -p build
make html

%install
cd Popularity/DCAFPilot
mkdir -p %i/etc
cp -r etc/* %i/etc
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
cp -r src/python/VW %i/lib/python*/site-packages

mkdir -p %i/doc
tar --exclude '.buildinfo' -C doc/build/html -cf - . | tar -C %i/doc -xvf -

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
