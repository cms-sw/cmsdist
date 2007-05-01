### RPM external heppdt 2.03.00
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{v}.tar.gz
%prep
%setup -q -n HepPDT-%{v}
./configure  --prefix=%{i} 

%build
make 

%install
make install
