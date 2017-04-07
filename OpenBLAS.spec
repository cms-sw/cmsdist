### RPM external OpenBLAS 0.2.19
Source: https://github.com/xianyi/OpenBLAS/archive/v%{realversion}.tar.gz

%prep
%setup -n %{n}-%{realversion}

%build

# PRESCOTT is a generic x86-64 target https://github.com/xianyi/OpenBLAS/issues/685 
%ifarch x86_64
make %{makeprocesses} FC=gfortran BINARY=64 TARGET=PENRYN 
%else
make %{makeprocesses} FC=gfortran BINARY=64
%endif

%install
make install PREFIX=%i

