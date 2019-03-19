### RPM external vincia 2.2.04

Requires: pythia8

Source: https://www.hepforge.org/archive/vincia/%{n}-%{realversion}.tgz

%prep
%setup -q -n %{n}-%{realversion}

./configure --prefix=%i --with-pythia8=${PYTHIA8_ROOT} --enable-shared

%build
make %makeprocesses

%install
make install
