### RPM external openloops 2.1.0
%define tag 87acafc00fe37cbe29afd82f3356483eb9006435
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/openloops.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
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
./openloops libinstall %{_sourcedir}/openloops-user.coll

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
