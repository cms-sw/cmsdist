### RPM external psimd 2020-05-17
%define commit 072586a71b55b7f8c584153d223e95687148a900

Source0: git+https://github.com/Maratyszcza/psimd.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: gmake cmake

%prep
%setup -n %{n}-%{realversion}

%build
cd %{_builddir}
rm -rf build
mkdir build && cd build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_BUILD_TYPE=Release

%install
cd %{_builddir}/build
make install
