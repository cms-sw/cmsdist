### RPM external vecgeom v1.2.10
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
## INCLUDE cpp-standard
## INCLUDE microarch_flags

%define tag bf8de1e0c18fb7b33c0871fab244de00d2bb2a44
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: vecgeom-fix-vector
BuildRequires: cmake gmake
%define keep_archives true
%define vecgeom_backend Scalar
%define vecgeom_version %(echo %{realversion} | sed -e 's|^v||;s|-.*||')
%define build_flags %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
SEL_ARCH=$(echo '%{selected_microarch}' | sed 's|^-m||')
VECGEOM_VECTOR_INST="$(grep ' set(VECGEOM_ISAS ' CMakeLists.txt | tr ' ' '\n' | grep -E "^${SEL_ARCH}$")"
%endif
%endif
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DVecGeom_GIT_DESCRIBE="%{vecgeom_version};;" \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_CXX_FLAGS_RELEASE="-O2 -DNDEBUG" \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_C_FLAGS="%{build_flags}" \
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR="${VECGEOM_VECTOR_INST}" \
%endif
%endif
  -DVECGEOM_NO_SPECIALIZATION=ON \
  -DVECGEOM_BUILTIN_VECCORE=ON \
  -DVECGEOM_BACKEND=%{vecgeom_backend} \
  -DVECGEOM_GEANT4=OFF \
  -DVECGEOM_ROOT=OFF

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1
sed -i -e 's|set(VecCore_DIR .*|set(VecCore_DIR "%{i}/lib64/cmake/VecCore")|' %{i}/lib64/cmake/VecGeom/VecGeomConfig.cmake

%post
%{relocateConfig}lib64/cmake/VecGeom/VecGeomConfig.cmake
