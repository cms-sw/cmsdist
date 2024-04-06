### RPM external cepgen 1.2.3_gcc710

Source: https://github.com/cepgen/cepgen/archive/refs/tags/%{realversion}.tar.gz
Patch: cepgen_nopython_noroot

BuildRequires: cmake gmake
Requires: gsl OpenBLAS hepmc lhapdf pythia6 bz2lib zlib xz

%prep
%setup -n %{n}-%{realversion}
%patch -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

export GSL_DIR=${GSL_ROOT}
export OPENBLAS_DIR=${OPENBLAS_ROOT}
export HEPMC_DIR=${HEPMC_ROOT}
export LHAPDF_PATH=${LHAPDF_ROOT}
export PYTHIA6_DIR=${PYTHIA6_ROOT}

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_PREFIX_PATH="${BZ2LIB_ROOT};${ZLIB_ROOT};${XZ_ROOT}"

make %{makeprocesses}

%install
cd ../build
make install

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
rm -f %i/lib/libCepGen*-[A-Z]*-%realversion.$so

%post
%{relocateConfig}bin/cepgen
