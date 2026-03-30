### RPM external highfive 2.10.1

%define github_user BlueBrain
%define branch master
%define tag ede97c8d51905c1640038561d12d41da173012ac
Source: git+https://github.com/%github_user/HighFive.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: highfive-boost190
BuildRequires: cmake
Requires: boost hdf5

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

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
