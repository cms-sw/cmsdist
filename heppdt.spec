### RPM external heppdt 2.03.00-CMS3
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
./configure  --prefix=%{i} 

%build
make 

%install
make install
