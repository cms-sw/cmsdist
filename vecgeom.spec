### RPM external vecgeom v1.2.1
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
%define tag 12fc8ba12efe93de5aaa9ff8e51e093ae93a1633
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true
%define vecgeom_backend Scalar
Patch0: vecgeom-fix-vector

%define build_flags %{?arch_build_flags} %{?lto_build_flags} %{?pgo_build_flags}

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_CXX_STANDARD:STRING="17" \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CXX_FLAGS_RELEASE="-O2 -DNDEBUG" \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_STATIC_LIBRARY_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_STATIC_LIBRARY_C_FLAGS="%{build_flags}" \
  -DCMAKE_CXX_FLAGS="%{build_flags}" \
  -DCMAKE_C_FLAGS="%{build_flags}" \
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR=sse3 \
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
