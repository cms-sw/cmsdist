### RPM external eigen 5.0.1
## INITENV +PATH PKG_CONFIG_PATH %{i}/share/pkgconfig
## NOCOMPILER
## INCLUDE cpp-standard
Source0: git+https://gitlab.com/libeigen/eigen.git?tag=%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
# Silence unused variable warning under NDEBUG in triangular_solve_over_reach_iter
Source1: https://gitlab.com/libeigen/eigen/-/commit/cae72577d966aa48593f68b5e030aca8f51c4939.patch
Patch0: eigen-const-scalar-operand
BuildRequires: cmake

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
patch -p1 -i %{SOURCE1}

%build
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DBUILD_TESTING=OFF -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} ../

%install
cd build
make install

%post
%{relocateConfig}share/pkgconfig/eigen3.pc
