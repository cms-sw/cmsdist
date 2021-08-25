### RPM external openloops 2.1.2
%define tag 4247179369144b0134c7b8014a5d38a90dc9b6ba
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%{github_user}/openloops.git?obj=%{branch}/%{tag}&export=openloops-%{openloop_version}&output=/openloops-%{openloop_version}-%{tag}.tgz
Source1: openloops-user.coll
BuildRequires: python scons

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

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
export SCONSFLAGS="-j %{compiling_processes}"
./openloops update --processes generator=0
./openloops libinstall lhc.coll
./openloops libinstall %{_sourcedir}/openloops-user.coll

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
