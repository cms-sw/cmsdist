### RPM external h5cpp 0.4.0

Source: https://github.com/ess-dmsc/h5cpp/archive/v%{realversion}.tar.gz
BuildRequires: gmake cmake
Requires: boost hdf5

%prep
%setup -n %{n}-%{realversion}

%build

cd %{_builddir}/
rm -rf build && mkdir build && cd build

cmake ../%{n}-%{realversion} \
		-DCONAN:STRING="DISABLE" \
		-DCMAKE_INSTALL_LIBDIR=lib \
		-DHDF5_INCLUDE_DIRS="${HDF5_ROOT}/include" \
		-DMPI_CXX_INCLUDE_PATH="${OPENMPI_ROOT}/include" \
		-DCMAKE_INSTALL_PREFIX=%{i} \
		-DCMAKE_PREFIX_PATH="${HDF5_ROOT};${BOOST_ROOT};${OPENMPI_ROOT}"

make %{makeprocesses}

%install

cd %{_builddir}/build
make install

