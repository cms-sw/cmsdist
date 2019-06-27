### RPM external opencl-cpp 1.1
## NOCOMPILER

Source0: http://www.khronos.org/registry/cl/api/%{realversion}/cl.hpp

Requires: opencl

%prep
# NOP

%build
# NOP

%install
mkdir -p %{i}/include/CL
cp %{SOURCE0} %{i}/include/CL
# bla bla
