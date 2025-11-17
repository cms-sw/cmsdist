### RPM external vecgeom v2.0.0-rc.8
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
## INCLUDE cpp-standard
## INCLUDE microarch_flags
## INCLUDE cuda-flags

%define tag %{realversion}
%define branch master
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: vecgeom-fix-vector
BuildRequires: cmake gmake
Requires: xerces-c
%{!?without_cuda:Requires: cuda}
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
  -DBUILD_TESTING=OFF \
  -DVecGeom_VERSION=%{vecgeom_version} \
  -DCMAKE_CXX_STANDARD:STRING="%{cms_cxx_standard}" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
  -DCMAKE_CXX_FLAGS_RELEASE="-O2 -DNDEBUG %{build_flags}" \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_C_FLAGS="%{build_flags}" \
%if 0%{!?without_cuda:1}
  -DCMAKE_CUDA_ARCHITECTURES=$(echo %{cuda_arch} | tr ' ' ';' | sed 's|;;*|;|') \
  -DVECGEOM_ENABLE_CUDA=ON \
%endif
  -DVECGEOM_GDML=ON \
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR="${VECGEOM_VECTOR_INST}" \
%endif
%endif
  -DVECGEOM_NO_SPECIALIZATION=ON \
  -DVECGEOM_BUILTIN_VECCORE=ON \
  -DVECGEOM_BACKEND=%{vecgeom_backend} \
  -DVECGEOM_GEANT4=OFF \
  -DVECGEOM_ROOT=OFF \
  -DCMAKE_PREFIX_PATH="${XERCES_C_ROOT}"

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1
sed -i -e 's|set(VecCore_DIR .*|set(VecCore_DIR "%{i}/lib64/cmake/VecCore")|' %{i}/lib64/cmake/VecGeom/VecGeomConfig.cmake

%post
%{relocateConfig}lib64/cmake/VecGeom/VecGeomConfig.cmake
