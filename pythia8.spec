### RPM external pythia8 212

Requires: hepmc lhapdf

%define tag 2c5a4f204767dfd62849eb01c9b70b4ff16311a9
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -q -n %{n}-%{realversion}

./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-lhapdf5=${LHAPDF_ROOT}

%build
make 

%install
make install
