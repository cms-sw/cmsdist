### RPM external hepmc 2.06.07
Source: http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-%realversion.tar.gz
Patch0: hepmc-2.03.06-reflex
Patch1: hepmc-2.06.07-WeightContainer-fix-size_type
Patch2: HepMC-2.06.07-nodoc

Requires: autotools

%define keep_archives true
%define drop_files %i/share

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n HepMC-%{realversion}
%patch0 -p0
%patch1 -p1
%patch2 -p1

F77="$(which gfortran) -fPIC"
CXX="$(which %{cms_cxx}) -fPIC"
PLATF_CONFIG_OPTS="--enable-static --disable-shared"

perl -p -i -e 's|glibtoolize|libtoolize|g' ./bootstrap

export HEPMC_NODOC=1

./bootstrap
./configure $PLATF_CONFIG_OPTS --prefix=%{i} --with-momentum=GEV --with-length=MM F77="$F77" CXX="$CXX" CXXFLAGS="%cms_cxxflags"

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
