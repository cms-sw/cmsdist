### RPM external vecgeom v1.1.2
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true

Patch0: vecgeom-fix-for-arm64

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DROOT=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_SPECIALIZATION=ON \
  -DBACKEND=Scalar \
  -DUSOLIDS=ON \
  -DUSOLIDS_VECGEOM=ON \
%ifarch x86_64
  -DVECGEOM_VECTOR=sse3 \
%else
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_CXX_STANDARD=17 \
%endif
  -DGEANT4=OFF

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/USolids/*.cmake
%{relocateConfig}lib/cmake/VecCore/*.cmake
%{relocateConfig}lib/cmake/VecGeom/*.cmake

