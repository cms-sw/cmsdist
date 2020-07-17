### RPM cms acdcserver 1.4.0.pre3
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

Source: git://github.com/dmwm/WMCore.git?obj=master/%{realversion}&export=%n&output=/%n.tar.gz
Requires: python py2-httplib2 rotatelogs couchdb15 py2-sphinx

%prep
%setup -b 0 -n %n

%build
python setup.py build_system -s acdcserver

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s acdcserver --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pf %_builddir/%n/bin/acdcserver-tools %i/bin

%post
