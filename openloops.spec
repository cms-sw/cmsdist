### RPM external openloops 1.2.3
%define tag 964f10ca45441599965541b60e82db55b03feb89
%define branch cms/v%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/openloops.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: python

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

%build
cat << \EOF >> openloops.cfg
[OpenLoops]
fortran_compiler = gfortran
gfortran_f90_flags = -ffixed-line-length-0 -ffree-line-length-0 -O0
loop_optimisation = -O0
generic_optimisation = -O0
born_optimisation = -O0
EOF

./openloops update --processes generator=0

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
