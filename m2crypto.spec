### RPM external m2crypto 0.15
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
%define pydir %(which python| python -c "import sys,os; version=sys.version[:3];path='/'+reduce(lambda x,y: x+y+'/',sys.stdin.readline().split('/')[:-2]);print path")
%define bindir %pydir/bin
%define sitedir %pydir/lib/python%pythonv/site-packages
## INITENV +PATH PYTHONPATH %{i}/lib

Summary: Support for using OpenSSL in python scripts.
Source: http://julian.ultralight.org/clarens/devel/%n-%v.tar.gz
Patch1: m2crypto-0.13.verify
Patch2: m2crypto-0.11.getkey
Patch3: m2crypto-swig-1.3.19-rh9
Patch5: m2crypto-makefile2
Patch6: m2crypto-0.13p1
Patch7: m2crypto-0.13.x509
Patch8: m2crypto-0.13.rsapem
Patch9: m2crypto-0.15-m2crypto
Patch10: m2crypto-makefile3

Group: System Environment/Libraries
URL: http://www.post1.com/home/ngps/m2/
Obsoletes: openssl-python

Requires: openssl python
%description
This package allows you to call OpenSSL functions from python scripts.


%prep


%setup -n m2crypto-%v -q

#%patch2 -p0 
%patch5 -p0 
#%patch6 -p0 
#%patch7 -p0 
#%patch8 -p0 
%patch9 -p0
%patch10 -p0

%build
cd SWIG
export opkg_root=$OPENSSL_ROOT
make PYINCLUDE="-DHAVE_CONFIG_H -I%pydir/include/python%pythonv" \
     PYLIB=%pydir/lib/python/config PYVER=%pythonv
cd ..

%install
cd M2Crypto
# Install the python extensions.
for subdir in `find -name "*.py" -o -name "*.so" | xargs -n1 dirname | sort -u`
do
	mkdir -p %i/lib/M2Crypto/${subdir}
done
find -name "*.py" | xargs -i install -m644 '{}' %i/lib/M2Crypto/'{}'
find -name "*.so" | xargs -i install -m755 '{}' %i/lib/M2Crypto/'{}'
#python -c "import compileall; compileall.compile_dir('"%i/lib/M2Crypto"', 3, '%sitedir/M2Crypto')"
cd ..


%files
%i
