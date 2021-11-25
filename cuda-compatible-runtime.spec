### RPM external cuda-compatible-runtime 1.0

%define branch master
%define commit bfe5537537428ab4a72ae929c77977a55501c576

Source: git+https://:@gitlab.cern.ch:8443/cms-patatrack/%{n}.git?obj=%{branch}/%{commit}&export=%{n}&filter=./test.cu&output=/%{n}-%{realversion}.tgz
Requires: cuda
AutoReq: no

%prep
%setup -n %{n}

%build
## INCLUDE cuda-flags
# defines nvcc_stdcxx and cuda_flags_4

rm -rf %{_builddir}/build && mkdir %{_builddir}/build
if
  $CUDA_ROOT/bin/nvcc %{nvcc_stdcxx} -O2 -g %{cuda_flags_4} test.cu -I $CUDA_ROOT/include -L $CUDA_ROOT/lib64 -L $CUDA_ROOT/lib64/stubs --cudart static -ldl -lrt --compiler-options '-Wall -pthread' -o %{_builddir}/build/cuda-compatible-runtime
then
  true
else
  # CUDA is not supported by this architecture or compiler version
  cat > %{_builddir}/build/cuda-compatible-runtime << @EOF_
#! /bin/bash

VERBOSE=false

function usage() {
  cat << @EOF
Usage: \$0 [-h|-v]

Options:
  -h        Print a help message and exits.
  -v        Be more verbose.
@EOF
}

for ARG in "\$@"; do
  case "\$ARG" in
  -h)
    usage
    exit 0
    ;;
  -v)
    VERBOSE=true
    ;;
  *)
    echo "\$0: invalid option '\$ARG'"
    echo
    usage
    exit 1
    ;;
  esac
done

\$VERBOSE && echo "CUDA ${CUDA_VERSION} is not compatible with GCC ${GCC_VERSION}"
exit 1
@EOF_
  chmod +x %{_builddir}/build/cuda-compatible-runtime
fi

%install
mkdir %{i}/test
cp %{_builddir}/build/cuda-compatible-runtime %{i}/test/cuda-compatible-runtime

%post
