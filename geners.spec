### RPM external geners 1.1.2

Source: http://www.hepforge.org/archive/geners/%{n}-%{realversion}.tar.gz

BuildRequires: autotools

Requires: zlib
Requires: bz2lib

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}-%{realversion}

# Enable C++11 for all compilers
cp ./geners/CPP11_config_enable.hh ./geners/CPP11_config.hh

./configure \
  --with-pic \
  --with-bzip2-include-path=${BZ2LIB_ROOT}/include \
  --with-bzip2-lib-path=${BZ2LIB_ROOT}/lib \
  --with-zlib-include-path=${ZLIB_ROOT}/include \
  --with-zlib-lib-path=${ZLIB_ROOT}/lib \
  --prefix=%{i} \
  CXX="%cms_cxx" \
  CXXFLAGS="%cms_cxxflags"

%build
make

%install
make install
