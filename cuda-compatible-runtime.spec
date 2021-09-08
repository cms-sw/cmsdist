### RPM external cuda-compatible-runtime 1.0

%define branch master
%define commit 18d5a51bfb32fbb7b765dd2eecd14e193cce8126

Source: git+https://:@gitlab.cern.ch:8443/cms-patatrack/%{n}.git?obj=%{branch}/%{commit}&export=%{n}&filter=./test.c&output=/%{n}-%{realversion}.tgz
Requires: cuda
AutoReq: no

%prep
%setup -n %{n}

%build
rm -rf %{_builddir}/build && mkdir %{_builddir}/build
gcc -std=c99 -O2 -Wall test.c -I $CUDA_ROOT/include -L $CUDA_ROOT/lib64 -L $CUDA_ROOT/lib64/stubs -l cudart_static -l cuda -ldl -lrt -pthread -static-libgcc -o %{_builddir}/build/cuda-compatible-runtime # || true

%install

mkdir %{i}/test
if [ -f %{_builddir}/build/cuda-compatible-runtime ]; then
  cp %{_builddir}/build/cuda-compatible-runtime %{i}/test/cuda-compatible-runtime
else
  ln -s /usr/bin/false %{i}/test/cuda-compatible-runtime
fi

%post
