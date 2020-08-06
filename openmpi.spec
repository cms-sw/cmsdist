### RPM external openmpi 4.0.4
## INITENV SET OPAL_PREFIX %{i}
Source: http://download.open-mpi.org/release/open-mpi/v4.0/%{n}-%{realversion}.tar.gz
BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}

./autogen.pl --force
./configure --prefix=%i --without-lsf --disable-libnuma --enable-mpi-cxx --enable-mpi-thread-multiple

%build
make %{makeprocesses} 

%install
make install
