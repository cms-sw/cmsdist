### RPM external hepmc3 3.2.7
## INCLUDE cpp-standard
Source: https://gitlab.cern.ch/hepmc/HepMC3/-/archive/%{realversion}/HepMC3-%{realversion}.tar.gz

BuildRequires: cmake

%define drop_files %i/share/doc

%prep
%setup -q -n HepMC3-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../HepMC3-%{realversion} \
  -DCMAKE_INSTALL_PREFIX="%i" \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
  -DHEPMC3_CXX_STANDARD=%{cms_cxx_standard} \
  -DHEPMC3_ENABLE_ROOTIO="OFF" \
  -DHEPMC3_ENABLE_TEST="OFF" \
  -DHEPMC3_ENABLE_PYTHON="OFF" \
  -DHEPMC3_BUILD_STATIC_LIBS="OFF" \
  -DHEPMC3_BUILD_DOCS="OFF" \
  -DHEPMC3_INSTALL_INTERFACES="ON" \
  -L

make %{makeprocesses}

%install
cd ../build
make install
