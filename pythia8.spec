### RPM external pythia8 306

%define tag b603a507960b8d0faa987dae28bdac948aaac9f6
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}%{realversion}&output=/%{n}-%{realversion}.tgz

Requires: hepmc hepmc3 lhapdf

%prep
%setup -q -n %{n}%{realversion}

./configure --prefix=%i --enable-shared --with-hepmc2=${HEPMC_ROOT} --with-hepmc3=${HEPMC3_ROOT} --with-lhapdf6=${LHAPDF_ROOT} --enable-mg5mes

%build
make %makeprocesses

%install
make install
test -f %i/lib/libpythia8lhapdf6.so || exit 1
rm -rf %{i}/share/Pythia8/examples

%post
%{relocateConfig}bin/pythia8-config
