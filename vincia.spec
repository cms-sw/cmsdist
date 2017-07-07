### RPM external vincia 1.2.02

Requires: pythia8

Source: https://www.hepforge.org/archive/vincia/%{n}-%{realversion}.tgz

%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

./configure --prefix=%i --with-pythia8=${PYTHIA8_ROOT}

# For version 2 "FFLAGS..." below can be substituted by --fc-common=-fPIC in the configure arguments above

%build
make %makeprocesses FFLAGS="-fPIC"

%install
make install
