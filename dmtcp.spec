### RPM external dmtcp 2.0-2212

%define pkg_version %(echo "%{realversion}" | cut -d- -f 1)
%define pkg_revision %(echo "%{realversion}" | cut -d- -f 2)

Source: svn://svn.code.sf.net/p/dmtcp/code/trunk?scheme=svn&revision=%{pkg_revision}&module=%{n}&output=/%{n}.tar.gz

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx g++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++11
%endif

%define drop_files %{i}/share

%prep
%setup -n %{n}

%build
./configure \
  --prefix=%{i} \
  --disable-test-suite \
  --disable-dependency-tracking \
  CXX="%{cms_cxx}" \
  CXXFLAGS="%{cms_cxxflags}"

make %{makeprocesses}

%install

make install
