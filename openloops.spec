### RPM external openloops 2.0.0
%define tag df5dc23c322dd460c4f8f3cdfa331bb190c647f6
%define branch cms/v%{realversion}
%define github_user cms-externals

Source: git+https://github.com/%github_user/openloops.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: python scons

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
#change the repo from remote to local files
sed -i -e 's|http:/|%{_builddir}/localrepo|' pyol/config/default.cfg

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

#get remote repo data locally, for 7_1 urllib2.urlopen uses ssl version which fails the communication with the server
wget -r -np --reject "index.html*" https://www.physik.uzh.ch/data/openloops/repositories/public/processes/ -P %{_builddir}/localrepo
wget -r -np --reject "index.html*" https://www.physik.uzh.ch/data/openloops/repositories/public/collections/ -P  %{_builddir}/localrepo
#build the libs
./openloops libinstall all.coll

%install
mkdir %i/{lib,proclib}
cp lib/*.so %i/lib
cp proclib/*.so %i/proclib
cp proclib/*.info %i/proclib
