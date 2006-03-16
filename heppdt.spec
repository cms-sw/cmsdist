### RPM external heppdt 2.02.02
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{v}.tar.gz
%prep
%setup -q -n HepPDT-%{v}
./configure  --prefix=%{i} 

%build
make 

%install
make install
