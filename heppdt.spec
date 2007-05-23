### RPM external heppdt 2.03.00-XXXX
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz

%prep
%setup -q -n HepPDT-%{realversion}
./configure  --prefix=%{i} 

%build
make 

%install
make install
