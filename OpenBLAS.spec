### RPM external OpenBLAS 0.3.5
Source: https://github.com/xianyi/OpenBLAS/archive/v%{realversion}.tar.gz

# Will be part of future release

%prep
%setup -n %{n}-%{realversion}

%build

# PRESCOTT is a generic x86-64 target https://github.com/xianyi/OpenBLAS/issues/685 
%ifarch x86_64
make FC=gfortran BINARY=64 TARGET=PENRYN NUM_THREADS=256 DYNAMIC_ARCH=0
%else
%ifarch aarch64
make FC=gfortran BINARY=64 TARGET=ARMV8 NUM_THREADS=256 DYNAMIC_ARCH=0
%else
make FC=gfortran BINARY=64 NUM_THREADS=256 DYNAMIC_ARCH=0
%endif # aarch64
%endif # x86_64

%install
make install PREFIX=%i

