### RPM external open-mpi 2.1.0
Source: https://github.com/open-mpi/ompi/archive/v%{realversion}.tar.gz


%prep
%setup -n %{n}-%{realversion}

%build

./configure
make %{makeprocesses} 

%install
make install PREFIX=%i

