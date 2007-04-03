### RPM external herwig 6.510
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{v}-src.tgz
Requires: gcc-wrapper
%define gccwrapperarch slc4_ia32_gcc345
%prep
%setup -q -n %n
./configure 

%build
%if "%{cmsplatf}" == "%{gccwrapperarch}"
echo "Using gcc wrapper for %cmsplatf"
source $GCC_WRAPPER_ROOT/etc/profile.d/init.sh
%endif
make 

%install
tar -c lib bin | tar -x -C %i

