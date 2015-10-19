### RPM external gmp-static 5.1.3

Source: ftp://ftp.gnu.org/gnu/gmp/gmp-%{realversion}.tar.bz2
Patch0: gmp-5.1.3-gcc49

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
%patch0 -p1

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
