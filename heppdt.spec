### RPM external heppdt 3.03.00
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner
Patch2: heppdt-3.03.00-silence-debug-output 
%define keep_archives yes

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
%patch2 -p1

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure  --prefix=%{i}

%build
make 

%install
make install
