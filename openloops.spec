### RPM external openloops 2.0.0
%define tag 944f9f27fc68d2a14d6df9f877ab49258028c7e6
%define branch cms/v%{realversion}
%define github_user cms-externals

Source: git+https://github.com/%github_user/openloops.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

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

./openloops update --processes generator=0

%install
mkdir %i/lib
cp lib/*.so %i/lib
