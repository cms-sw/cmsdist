### RPM external cuda-compatible-runtime 2.0

%define branch master
%define commit 8069d15b0979cd4ec5c821960feb066a1e03f8ce

Source: git+https://github.com/cms-patatrack/%{n}.git?obj=%{branch}/%{commit}&export=%{n}&filter=./test.cu&output=/%{n}-%{realversion}.tgz
Requires: cuda

%prep
%setup -n %{n}

%build
## INCLUDE cuda-flags
# defines nvcc_flags_stdcxx and nvcc_flags_cuda_archs

rm -rf %{_builddir}/build && mkdir %{_builddir}/build
if
  $CUDA_ROOT/bin/nvcc %{nvcc_flags_stdcxx} -O2 -g %{nvcc_flags_cuda_archs} test.cu -I $CUDA_ROOT/include -L $CUDA_ROOT/lib64 -L $CUDA_ROOT/lib64/stubs --cudart static -ldl -lrt --compiler-options '-Wall -pthread' -o %{_builddir}/build/cuda-compatible-runtime
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
