### RPM external pythia8 212

Requires: hepmc lhapdf

%define tag fb369df55af7e8431d6b8f984d09b906a030109a
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -q -n %{n}-%{realversion}

export USRCXXFLAGS="%cms_cxxflags"
./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf6=${LHAPDF_ROOT}

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
