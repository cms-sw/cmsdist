### RPM external py2-pymongo 1.8.1
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pypi.python.org/packages/source/p/pymongo/pymongo-%realversion.tar.gz
Requires: python elementtree

%prep
%setup -n pymongo-%realversion

%build

%install
mkdir -p %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
python setup.py build
#build builds lib.linux-i686-2.6
mv build/lib*/* %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

# setup dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
