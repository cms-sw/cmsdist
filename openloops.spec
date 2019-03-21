### RPM external openloops 2.0.0
%define tag a0fd88934c5c5b83f66fa4791c07f7872ec00a13
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: http://www.hepforge.org/archive/openloops/OpenLoops-2.0.0.tar.gz

BuildRequires: python scons

#Patch0: openloops-1.2.3-cpp-use-undef

%define keep_archives true

%prep
%setup -n OpenLoops-%{realversion}
#%patch0 -p1

%build
cat << \EOF >> openloops.cfg
[OpenLoops]
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0
generic_optimisation = -O2
born_optimisation = -O2
loop_optimisation = -O0
link_optimisation = -O2
EOF

./openloops update --processes generator=0

%install
#mkdir %i/{lib,proclib}
mkdir %i/lib
cp lib/*.so %i/lib
#cp proclib/*.so %i/proclib
#cp proclib/*.info %i/proclib
