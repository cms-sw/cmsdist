### RPM external hepmc3 3.3.1
## INCLUDE cpp-standard
Source: https://gitlab.cern.ch/hepmc/HepMC3/-/archive/%{realversion}/HepMC3-%{realversion}.tar.gz

BuildRequires: cmake gmake
Requires: zlib bz2lib xz zstd

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
  -DHEPMC3_ENABLE_TEST="ON" \
  -DHEPMC3_TEST_THREADS="ON" \
  -DHEPMC3_TEST_HEPMC2="OFF" \
  -DHEPMC3_TEST_VALGRIND="OFF" \
  -DHEPMC3_TEST_ZLIB="ON" \
  -DHEPMC3_TEST_LZMA="ON" \
  -DHEPMC3_TEST_BZIP2="ON" \
  -DHEPMC3_TEST_ZSTD="ON" \
  -DHEPMC3_ENABLE_PYTHON="OFF" \
  -DHEPMC3_BUILD_STATIC_LIBS="OFF" \
  -DHEPMC3_BUILD_DOCS="OFF" \
  -DHEPMC3_INSTALL_INTERFACES="ON" \
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}" \
  -L

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install
