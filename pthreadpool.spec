### RPM external pthreadpool 2021-04-13

%define commit a134dd5d4cee80cce15db81a72e7f929d71dd413
%define fxdiv_commit 63058eff77e11aa15bf531df5dd34395ec3017c8

BuildRequires: cmake python

Source0: git+https://github.com/Maratyszcza/pthreadpool.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Source1: git+https://github.com/Maratyszcza/fxdiv.git?obj=master/%{fxdiv_commit}&export=fxdiv-%{fxdiv_commit}&output=/fxdiv-%{fxdiv_commit}.tgz

%prep
%setup -n %{n}-%{realversion}
%setup -a1 -n fxdiv

%build
cd %{_builddir}
rm -rf build; mkdir -p build; cd build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_BUILD_TYPE=Release \
    -DFXDIV_SOURCE_DIR=%{_sourcedir}/fxdiv \
    -DBUILD_SHARED_LIBS=ON \
    -DPTHREADPOOL_BUILD_TESTS=OFF \
    -DPTHREADPOOL_BUILD_BENCHMARKS=OFF

%install
%make
cd %{_builddir}
make install
