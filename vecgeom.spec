### RPM external vecgeom v00.05.00
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

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
  -DVECGEOM_VECTOR=sse3 \
  -DGEANT4=OFF

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/USolids/*.cmake
%{relocateConfig}lib/cmake/VecCore/*.cmake
%{relocateConfig}lib/cmake/VecGeom/*.cmake

