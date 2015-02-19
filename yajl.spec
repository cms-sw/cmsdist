### RPM external yajl 1.0.9
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source: https://github.com/downloads/lloyd/yajl/yajl-%{realversion}.tar.gz
Requires: cmake

%prep
%setup -n yajl-%realversion

%build
mkdir build
cd build
cmake ..
make

%install
cp -r build/yajl-%{realversion}/* %i/
cp -r src %i/
%define drop_files %i/share/doc
