### RPM external form 4.2.1
Source: https://github.com/vermaseren/form/releases/download/v%{realversion}/form-%{realversion}.tar.gz
BuildRequires: gmake
Requires: zlib

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%prep
%setup -q -n form-%{realversion}

%build

CXX="$(which %{cms_cxx})"
CC="$(which gcc)"

./configure --prefix=%i \
            --bindir=%i/bin \
            --without-gmp \
            --with-zlib=${ZLIB_ROOT} \
            CXX="$CXX" CC="$CC" CXXFLAGS=-fpermissive

make %makeprocesses

%install
make install
