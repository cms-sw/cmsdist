### RPM external openmpi 1.6.5
Source: http://www.open-mpi.org/software/ompi/v1.6/downloads/%{n}-%{realversion}.tar.gz 
%prep
%setup -q -n %{n}-%{realversion}

./configure --prefix=%i --disable-vt 

%build

make %{makeprocesses} 

%install
make install
