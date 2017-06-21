### RPM external openmpi 2.1.1
Source: http://www.open-mpi.org/software/ompi/v2.1/downloads/%{n}-%{realversion}.tar.gz 
Patch1: openmpi-2.1.1-disable-lsf-support
BuildRequires: autotools
%prep
%setup -q -n %{n}-%{realversion}
%patch1 -p1
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env/perl|' ./opal/asm/generate-asm.pl
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env/perl|' opal/asm/generate-all-asm.pl
sed -i -e 's|/usr/bin/perl|/usr/bin/env/perl|' ./Doxyfile
sed -i -e 's|/usr/bin/perl|/usr/bin/env/perl|' ./orte/Doxyfile

./configure --prefix=%i --without-lsf

%build
make %{makeprocesses} 

%install
make install
