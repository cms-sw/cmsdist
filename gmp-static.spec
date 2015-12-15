### RPM external gmp-static 6.1.0

Source: http://davidlt.web.cern.ch/davidlt/vault/gmp-%{realversion}.tar.bz2

BuildRequires: autotools

%define keep_archives true
%define drop_files %{i}/share

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%prep
%setup -n gmp-%{realversion}

%build
./configure \
  --prefix=%{i} \
  --build=%{_build} \
  --host=%{_host} \
  --disable-shared \
  --enable-static \
  --enable-cxx \
  --with-pic \
  CXX="%{cms_cxx}" \
  CXXFLAGS="%{cms_cxxflags}"

make %{makeprocesses}

%install

make install
find %{i}/lib -name '*.la' -delete
