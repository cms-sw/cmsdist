### RPM external cudnn 8.1.1.33
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define cudaver 11.2
%define cudnnver_maj %(echo %{realversion} | cut -f1,2,3 -d.)

%ifarch x86_64
Source: https://developer.download.nvidia.com/compute/redist/cudnn/v%{cudnnver_maj}/cudnn-%{cudaver}-linux-x64-v%{realversion}.tgz
%endif
%ifarch ppc64le
Source: https://developer.download.nvidia.com/compute/redist/cudnn/v%{cudnnver_maj}/cudnn-%{cudaver}-linux-ppc64le-v%{realversion}.tgz
%endif
%ifarch aarch64
Source: https://developer.download.nvidia.com/compute/redist/cudnn/v%{cudnnver_maj}/cudnn-%{cudaver}-linux-aarch64sbsa-v%{realversion}.tgz
%endif
Requires: cuda

%prep
%setup -n cuda

if [ "${CUDA_VERSION%.*}" != %{cudaver} ]; then
    echo 'Incompatible CUDA version in cudnn.spec!'
    exit 1
fi

%build

%install
rm %_builddir/cuda/lib64/*.a
mv %_builddir/cuda/* %{i}/

