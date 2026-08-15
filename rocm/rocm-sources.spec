## INCLUDE rocm/version
### RPM external rocm-sources %{rocm_version_num}
## NOCOMPILER
AutoReqProv: no
%define rocm_version therock-%{rocm_version_num}

Source0: git+https://github.com/ROCm/rocm-systems.git?obj=develop/%{rocm_version}&export=rocm-systems&submodules=1&output=/rocm-systems.tar.gz
Source1: git+https://github.com/ROCm/rocm-libraries.git?obj=develop/%{rocm_version}&export=rocm-libraries&submodules=1&output=/rocm-libraries.tar.gz

%prep

%build

%install
cp %{SOURCE0} %{i}/rocm_systems.tar.gz
cp %{SOURCE1} %{i}/rocm_libraries.tar.gz

%post
cd ${RPM_INSTALL_PREFIX}/%{pkgrel}
tar -xzvf rocm_systems.tar.gz
tar -xzvf rocm_libraries.tar.gz
