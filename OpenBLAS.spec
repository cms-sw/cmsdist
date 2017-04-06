### RPM external OpenBLAS 0.2.19
Source: https://github.com/xianyi/OpenBLAS/archive/v%{realversion}.tar.gz

# Will be part of future release
Patch0: a6e9e0b94b87f149b993bfefe99737b5f711f298
Patch1: 9e2f316ede9ee12441e9eb30784ceb653295b80a

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build

make %{makeprocesses} FC=gfortran BINARY=64 

%install
make install PREFIX=%i

