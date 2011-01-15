### RPM external yajl 1.0.9
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: https://github.com/downloads/lloyd/yajl/yajl-%{realversion}.tar.gz
Requires: cmake

%prep
%setup -n yajl-*

%build
mkdir build
cd build
cmake ..
make

%install
cp -r build/yajl-%{realversion}/* %i/
cp -r src %i/
