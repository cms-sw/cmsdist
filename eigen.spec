### RPM external eigen 01ae86b9aad30b1e65cf1b749fd6cd9a645ac00d
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## INITENV SETV EIGEN_SOURCE %{source0}
## INITENV SETV EIGEN_STRIP_PREFIX %{source_prefix}
## NOCOMPILER
%define tag %{realversion}

# These are needed by Tensorflow sources
# NOTE: Never apply any patch in the spec file, this way tensorflow gets the exact same sources
%define source0 https://github.com/cms-externals/eigen-git-mirror/archive/%{tag}.tar.gz
%define source_prefix eigen-git-mirror-%{realversion}
Source: %{source0}
BuildRequires: cmake

%prep
%setup -n %{source_prefix}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DBUILD_TESTING=OFF ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
