### RPM external dire 2.003

Requires: pythia8

Source: https://dire.gitlab.io/Downloads/DIRE-%{realversion}.tar.gz

%prep
%setup -q -n DIRE-%{realversion}

./configure --prefix=%i --with-pythia8=${PYTHIA8_ROOT} --enable-shared

%build
make %makeprocesses

%install
make install
ls %i/lib
