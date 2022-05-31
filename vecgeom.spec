### RPM external vecgeom v1.1.20
## INCLUDE compilation_flags
%define tag ccc45b15420e60f39b60107795a85fed12332005
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
Requires: veccore
%define keep_archives true
%define vecgeom_backend Scalar
Patch0: vecgeom-fix-vector

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=%{i}/lib \
  -DROOT=OFF \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_SPECIALIZATION=ON \
  -DBACKEND=%{vecgeom_backend} \
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR=sse3 \
%endif
%endif
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_CXX_STANDARD=17 \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="-fPIC %{arch_build_flags}" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="-fPIC %{arch_build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="-fPIC %{arch_build_flags}" \
%else
  -DCMAKE_CXX_FLAGS="-fPIC" \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="-fPIC" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="-fPIC" \
%endif
  -DGEANT4=OFF \
  -DDATA_DOWNLOAD=OFF \
  -DVecCore_DIR=${VECCORE_ROOT}/lib64/cmake/VecCore \
  -DCMAKE_PREFIX_PATH=${VECCORE_ROOT}

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/VecGeom/*.cmake
