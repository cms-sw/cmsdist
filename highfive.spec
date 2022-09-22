### RPM external highfive 2.3.1

%define github_user BlueBrain
%define branch master
%define tag a01ee6be4d4a75aeeb9fd962c3b415ea8cd395f6
Source: git+https://github.com/%github_user/HighFive.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: boost hdf5

%prep
%setup -n %{n}-%{realversion}

%build
cd %{_builddir}
rm -rf build
mkdir build && cd build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DHIGHFIVE_EXAMPLES=OFF \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DHIGHFIVE_UNIT_TESTS=OFF \
    -DCMAKE_PREFIX_PATH="${BOOST_ROOT};${HDF5_ROOT}"

%install
cd %{_builddir}/build
make install

%post
%{relocateConfig}share/HighFive/CMake/HighFiveTargets.cmake
