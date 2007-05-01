### RPM external jimmy 4.2
Requires: gcc-wrapper
Requires: herwig
%define gccwrapperarch slc4_ia32_gcc345
%define realversion %(echo %v | cut -d- -f1 )
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
%prep
%setup -q -n %{n}
./configure --with-herwig=$HERWIG_ROOT

%build
%if "%{cmsplatf}" == "%{gccwrapperarch}"
echo "Using gcc wrapper for %cmsplatf"
source $GCC_WRAPPER_ROOT/etc/profile.d/init.sh
%endif
make 

%install
tar -c lib include | tar -x -C %i

