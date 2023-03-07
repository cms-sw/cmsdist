### RPM external cudnn 8.8.0.121
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define cudaver 12

# NVIDIA uses sbsa for aarch64, and the standard architecture name for ppc64le and x86_64
%ifarch aarch64
%define nvarch sbsa
%else
%define nvarch %{_arch}
%endif

# cuDNN archive base name and unpacked name
%define archive cudnn-linux-%{nvarch}-%{realversion}_cuda%{cudaver}-archive

Source: https://developer.download.nvidia.com/compute/cudnn/redist/cudnn/linux-%{nvarch}/%{archive}.tar.xz
Requires: cuda

%prep
%setup -n %{archive}

if [ "${CUDA_VERSION%.*.*}" != %{cudaver} ]; then
    echo 'Incompatible CUDA version in cudnn.spec!'
    exit 1
fi

%build

%install
# onnxruntime is hardcoded to look for the cudnn libraries under .../lib64
mv %_builddir/%{archive}/lib %{i}/lib64
mv %_builddir/%{archive}/*   %{i}/
