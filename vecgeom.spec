### RPM external vecgeom v1.1.17
## INCLUDE compilation_flags
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
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_SPECIALIZATION=ON \
  -DBACKEND=Scalar \
%ifarch x86_64
  -DVECGEOM_VECTOR=sse3 \
%endif
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_CXX_STANDARD=17 \
%ifarch ppc64le
  -DCMAKE_CXX_FLAGS="%{ppc64le_build_flags}" \
%endif
  -DGEANT4=OFF

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/VecGeom/*.cmake
