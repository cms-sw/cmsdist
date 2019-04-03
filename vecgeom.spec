### RPM external vecgeom v00.05.00
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isaarch64 %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac)
%define isppc64 %(case %{cmsplatf} in (*_ppc64le_*) echo 1 ;; (*) echo 0 ;; esac)

Patch0: vecgeom-fix-for-arm64
Patch1: vecgeom-uninit-fix
Patch2: vecgeom-add-ppc64-cmake-fix

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1
%patch1 -p1
%if %isppc64
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
%if %isamd64
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

