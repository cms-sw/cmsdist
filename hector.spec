### RPM external Hector 1_3_1
Requires: gcc-wrapper
%define gccwrapperarch slc4_ia32_gcc345
Source: http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/Hector_%{v}.tbz

%prep
%setup -q -n %n

%build
## IMPORT gcc-wrapper
make 

%install
tar -c lib include | tar -x -C %i

