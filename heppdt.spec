### RPM external heppdt 3.03.00
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner
Patch2: heppdt-3.03.00-silence-debug-output 
%define keep_archives yes

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
%patch2 -p1
./configure  --prefix=%{i} 

%build
make 

%install
make install
