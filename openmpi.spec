### RPM external openmpi 2.1.5
## INITENV SET OPAL_PREFIX %{i}
Source: http://download.open-mpi.org/release/open-mpi/v2.1/%{n}-%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env perl|' ./opal/asm/generate-asm.pl
sed -i -e 's|#!/usr/bin/perl|#!/usr/bin/env perl|' opal/asm/generate-all-asm.pl
sed -i -e 's|/usr/bin/perl|/usr/bin/env perl|' ./Doxyfile
sed -i -e 's|/usr/bin/perl|/usr/bin/env perl|' ./orte/Doxyfile
./autogen.pl --force
./configure --prefix=%i --without-lsf --disable-libnuma --enable-mpi-cxx --enable-mpi-thread-multiple

%build
make %{makeprocesses} 

%install
make install
# bla bla
