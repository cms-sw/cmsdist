### RPM external openmpi 2.1.2rc4
## INITENV SET OPAL_PREFIX %{i}
Source: http://www.open-mpi.org/software/ompi/v2.1/downloads/%{n}-%{realversion}.tar.gz 
Patch1: openmpi-2.1.1-disable-lsf-support
BuildRequires: autotools
%prep
%setup -q -n %{n}-%{realversion}
%patch1 -p1
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env perl|' ./opal/asm/generate-asm.pl
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env perl|' opal/asm/generate-all-asm.pl
sed -i -e 's|/usr/bin/perl|/usr/bin/env perl|' ./Doxyfile
sed -i -e 's|/usr/bin/perl|/usr/bin/env perl|' ./orte/Doxyfile
./autogen.pl --force
./configure --prefix=%i --without-lsf --disable-libnuma --enable-mpi-cxx

%build
make %{makeprocesses} 

%install
make install
