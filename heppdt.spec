### RPM external heppdt 2.03.00
Requires: gcc-wrapper
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{v}.tar.gz
%prep
%setup -q -n HepPDT-%{v}
./configure  --prefix=%{i} 

%build
## IMPORT gcc-wrapper
make 

%install
make install
