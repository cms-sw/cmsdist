### RPM external OpenBLAS 0.3.15
## INCLUDE compilation_flags
Source: https://github.com/xianyi/OpenBLAS/archive/v%{realversion}.tar.gz
Patch0: OpenBLAS-fix-dynamic-arch
Patch1: OpenBLAS-disable-tests

# Will be part of future release

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build

# PRESCOTT is a generic x86-64 target https://github.com/xianyi/OpenBLAS/issues/685 
%define build_opts FC=gfortran BINARY=64 NUM_THREADS=256 DYNAMIC_ARCH=0 MAKE_NB_JOBS=%{compiling_processes}
%ifarch x86_64
make %{build_opts} TARGET=CORE2
%endif
%ifarch aarch64
make %{build_opts} TARGET=ARMV8 CFLAGS="%{arch_build_flags}"
%endif
%ifarch ppc64le
make %{build_opts} CFLAGS="%{arch_build_flags}"
%endif

%install
make install PREFIX=%i MAKE_NB_JOBS=%{compiling_processes}

%post
%relocateConfigAll lib/cmake *.cmake
