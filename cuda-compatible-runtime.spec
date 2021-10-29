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
$CUDA_ROOT/bin/nvcc %{nvcc_stdcxx} -O2 -g %{cuda_flags_4} test.cu -I $CUDA_ROOT/include -L $CUDA_ROOT/lib64 -L $CUDA_ROOT/lib64/stubs --cudart static -ldl -lrt --compiler-options '-Wall -pthread' -o %{_builddir}/build/cuda-compatible-runtime # || true


%install

mkdir %{i}/test
if [ -f %{_builddir}/build/cuda-compatible-runtime ]; then
  cp %{_builddir}/build/cuda-compatible-runtime %{i}/test/cuda-compatible-runtime
else
  ln -s /usr/bin/false %{i}/test/cuda-compatible-runtime
fi

%post
