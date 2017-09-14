### RPM external py3-pymongo 3.4.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

#Source: http://pypi.python.org/packages/source/p/pymongo/pymongo-%realversion.tar.gz
Source: https://pypi.python.org/packages/82/26/f45f95841de5164c48e2e03aff7f0702e22cef2336238d212d8f93e91ea8/pymongo-%realversion.tar.gz
Requires: python3 py3-elementtree
BuildRequires: py3-setuptools

%prep
%setup -n pymongo-%realversion

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
# replace all instances of #!/path/bin/python into proper format
for f in `find %i -type f`; do
    if [ -f $f ]; then
        perl -p -i -e 's{.*}{#!/usr/bin/env python3} if $. == 1 && m{#!.*/bin/python.*}' $f
    fi
done


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
