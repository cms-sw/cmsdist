### RPM external vecgeom v1.1.17
## INCLUDE compilation_flags
## INCLUDE compilation_flags_lto
%define tag ed9a40412c354652262ec80af449f5531206e52c
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true

Patch0: vecgeom-fix-vector

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DCMAKE_INSTALL_LIBDIR=%{i}/lib \
  -DROOT=OFF \
  -DCMAKE_AR=$(which gcc-ar) \
  -DCMAKE_RANLIB=$(which gcc-ranlib) \
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_SPECIALIZATION=ON \
  -DBACKEND=Scalar \
%ifarch x86_64
  -DVECGEOM_VECTOR=sse3 \
%endif
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_CXX_STANDARD=17 \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="%{arch_build_flags} %{lto_build_flags}" \
%else
  -DCMAKE_CXX_FLAGS="%{lto_build_flags}" \
%endif
  -DGEANT4=OFF

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make %{makeprocesses} install VERBOSE=1

%post
%{relocateConfig}lib/cmake/VecGeom/*.cmake
