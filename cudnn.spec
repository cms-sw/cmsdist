### RPM external cudnn 8.4.1.50
## INITENV +PATH LD_LIBRARY_PATH %i/lib64

%define cudaver 11.7
# cudnn 8.4.1 is defined for cuda 11.X and source default version is 11.6
%define default_cudaver 11.6
%define cudnnver_maj %(echo %{realversion} | cut -f1,2,3 -d.)

# NVIDIA uses sbsa for aarch64, and the standard architecture name for ppc64le and x86_64
%ifarch aarch64
%define nvarch sbsa
%else
%define nvarch %{_arch}
%endif

# cuDNN archive base name and unpacked name
%define archive cudnn-linux-%{nvarch}-%{realversion}_cuda%{default_cudaver}-archive

Source: https://developer.download.nvidia.com/compute/redist/cudnn/v%{cudnnver_maj}/local_installers/%{default_cudaver}/%{archive}.tar.xz
Requires: cuda

%prep
%setup -n %{archive}

if [ "${CUDA_VERSION%.*}" != %{cudaver} ]; then
    echo 'Incompatible CUDA version in cudnn.spec!'
    exit 1
fi

%build

%install
# onnxruntime is hardcoded to look for the cudnn libraries under .../lib64
mv %_builddir/%{archive}/lib %{i}/lib64
mv %_builddir/%{archive}/*   %{i}/
