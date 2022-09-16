### RPM external cepgen 1.0.2patch1

Source: https://github.com/cepgen/cepgen/archive/refs/tags/%{realversion}.tar.gz

BuildRequires: cmake ninja
Requires: gsl OpenBLAS hepmc hepmc3 lhapdf pythia6 root

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

export GSL_DIR=${GSL_ROOT}
export OPENBLAS_DIR=${OPENBLAS_ROOT}
export HEPMC_DIR=${HEPMC_ROOT}
export HEPMC3_DIR=${HEPMC3_ROOT}
export LHAPDF_PATH=${LHAPDF_ROOT}
export PYTHIA6_DIR=${PYTHIA6_ROOT}
export ROOTSYS=${ROOT_ROOT}

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_INSTALL_PREFIX:PATH="%i" \
  -DCMAKE_BUILD_TYPE=Release

ninja -v %{makeprocesses}

%install
cd ../build
ninja %{makeprocesses} install

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
rm -f %i/lib/libCepGen*-[A-Z]*-%realversion.$so

%post
%{relocateConfig}bin/cepgen
