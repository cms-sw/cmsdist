### RPM external openloops 1.0.0
Source: http://www.hepforge.org/archive/openloops/OpenLoops-%{realversion}.tar.gz

%prep

%setup -n OpenLoops-%{realversion}


cat << \EOF >> openloops.cfg
[OpenLoops]
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0
EOF

cat openloops.cfg

./scons auto=all/ 

%build

%install

mkdir %i/lib
mkdir %i/proclib
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
