### RPM external vecgeom v00.05.00
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true

Patch0: vecgeom-fix-for-arm64
Patch1: vecgeom-uninit-fix
Patch2: vecgeom-add-ppc64-cmake-fix

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1
%patch1 -p1
%ifarch ppc64le
%patch2 -p1
%endif

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
%ifarch ppc64le
  -DCMAKE_CXX_FLAGS="-mlong-double-64" \
%endif
  -DGEANT4=OFF

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install
perl -p -i -e 's|set\(VECGEOM_EXTERNAL_INCLUDES .*|set(VECGEOM_EXTERNAL_INCLUDES "")|' \
  $(grep -R 'set(VECGEOM_EXTERNAL_INCLUDES ' %{i}/lib/cmake | sed 's|:.*||' | sort | uniq)

%post
%{relocateConfig}lib/cmake/USolids/*.cmake
%{relocateConfig}lib/cmake/VecCore/*.cmake
%{relocateConfig}lib/cmake/VecGeom/*.cmake

