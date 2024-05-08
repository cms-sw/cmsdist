### RPM external OpenBLAS 0.3.15
## INCLUDE compilation_flags
## INCLUDE microarch_flags
Source: https://github.com/xianyi/OpenBLAS/archive/v%{realversion}.tar.gz
Patch0: OpenBLAS-fix-dynamic-arch
Patch1: OpenBLAS-disable-tests

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1

%build

%ifarch x86_64
XTARGETS="sse3=CORE2"
for t in nehalem sandybridge haswell ; do
  XTARGETS="${XTARGETS} $t=$(echo $t | tr 'a-z' 'A-Z')"
done
XTARGETS="${XTARGETS} skylake-avx512=SKYLAKEX"
XTARGETS="${XTARGETS} x86-64-v2=NEHALEM"
XTARGETS="${XTARGETS} x86-64-v3=HASWELL"
XTARGETS="${XTARGETS} x86-64-v4=SKYLAKEX"
STARGET=$(echo %{selected_microarch} | sed 's|^-m||;s|^arch=||')
TARGET_ARCH=$(echo ${XTARGETS} | tr ' ' '\n' | grep "^${STARGET}=" | sed "s|^${STARGET}=||")
if [ "${TARGET_ARCH}" == "" ] ; then
  echo "ERROR: Unable to match OpenBlas build target '${STARGET}'. Available build targets are"
  echo "${XTARGETS}" | tr ' ' '\n' | sed 's|=.*||'
  echo "Please use one of the supported targets or add support for $%{STARGET}'"
  exit 1
fi
%endif

# PRESCOTT is a generic x86-64 target https://github.com/xianyi/OpenBLAS/issues/685 
%define build_opts FC=gfortran BINARY=64 NUM_THREADS=256 DYNAMIC_ARCH=0 MAKE_NB_JOBS=%{compiling_processes}
%ifarch x86_64
make %{build_opts} TARGET=${TARGET_ARCH}
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
