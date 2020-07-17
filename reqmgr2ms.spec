### RPM cms reqmgr2ms 0.4.0.pre3
## INITENV +PATH PATH %i/xbin
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHONPATH %i/x${PYTHON_LIB_SITE_PACKAGES}

%define wmcorever 1.4.0.pre3

Source: git://github.com/dmwm/WMCore?obj=master/%wmcorever&export=%n&output=/%n.tar.gz
Requires: py2-cherrypy py2-pycurl py2-httplib2 py2-rucio-clients py2-retry py2-future
Requires: cmsmonitoring rotatelogs jemalloc mongo py2-pymongo
BuildRequires: py2-sphinx

%prep
%setup -b 0 -n %n 

%build
python setup.py build_system -s reqmgr2ms

%install
mkdir -p %i/{x,}{bin,lib,data,doc} %i/{x,}$PYTHON_LIB_SITE_PACKAGES
python setup.py install_system -s reqmgr2ms --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

mkdir -p %i/bin
cp -pfr %_builddir/%n/bin/[[:lower:]]* %i/bin

%post
