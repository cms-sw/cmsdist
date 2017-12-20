### RPM external pythia8 226

Requires: hepmc lhapdf
Requires: boost

%define tag 1dfa81bc0b3efa66793deb50b63eaf85d42e4dd2
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}-%{realversion}
 
export USRCXXFLAGS="%cms_cxxflags"
./configure --prefix=%i --enable-shared --with-boost=${BOOST_ROOT} --with-hepmc2=${HEPMC_ROOT} --with-lhapdf6=${LHAPDF_ROOT} --with-lhapdf6-plugin=LHAPDF6.h

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
