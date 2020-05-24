### RPM external openloops 2.1.1
%define tag 5284f172973c666ef7e58b56b180b8703d9fba13
%define branch cms/v2.1.1
%define github_user cms-externals
Source: git+https://github.com/%github_user/openloops.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Source1: openloops-user.coll
BuildRequires: python scons

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

%build
gcc10_extra_flag=""
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then export gcc10_extra_flag=-fallow-invalid-boz ; fi

cat <<EOF > openloops.cfg
[OpenLoops]
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0 $gcc10_extra_flag
generic_optimisation = -O2
born_optimisation = -O2
loop_optimisation = -O0
link_optimisation = -O2
EOF
export SCONSFLAGS="-j %{compiling_processes}"
./openloops update --processes generator=0
./openloops libinstall %{_sourcedir}/openloops-user.coll

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
