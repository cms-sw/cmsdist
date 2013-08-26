### RPM external gmp-static 5.0.2

Source: ftp://ftp.gnu.org/gnu/gmp/gmp-%{realversion}.tar.bz2

%define keep_archives true
%define drop_files %{i}/share

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n gmp-%{realversion}

%build
./configure \
  --prefix=%{i} \
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
