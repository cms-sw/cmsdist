### RPM external opencl-cpp 2.0.16
## NOCOMPILER
%define skip_license_checks 1
Source0: https://raw.githubusercontent.com/KhronosGroup/OpenCL-CLHPP/v%{realversion}/include/CL/opencl.hpp

Requires: opencl

%prep
# NOP

%build
# NOP

%install
mkdir -p %{i}/include/CL
cp %{SOURCE0} %{i}/include/CL
