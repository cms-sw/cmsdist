### RPM external hdf5 1.14.1
%define hdf5_tag hdf5-%(echo %realversion | tr '.' '_')
Source: https://github.com/HDFGroup/hdf5/archive/refs/tags/%{hdf5_tag}.tar.gz
Requires: zlib openmpi

%prep
%setup -n %{n}-%{hdf5_tag}

%build
rm -f ./bin/config.{sub,guess}
%get_config_sub ./bin/config.sub
%get_config_guess ./bin/config.guess
chmod +x ./bin/config.{sub,guess}
CXXFLAGS=-I${OPENMPI_ROOT}/include \
LDFLAGS="-L${OPENMPI_ROOT}/lib -lmpi" \
./configure --prefix %{i} \
            --disable-sharedlib-rpath \
            --disable-static--enable-shared \
            --enable-parallel \
            --enable-cxx --enable-unsupported --with-zlib=${ZLIB_ROOT}

make %{makeprocesses} V=1

%install
make install V=1

%post
%{relocateConfig}bin/h5pcc
%{relocateConfig}bin/h5c++
%{relocateConfig}share/hdf5_examples/c*/run-*-ex.sh
%{relocateConfig}share/hdf5_examples/hl/c*/run-*-ex.sh
%{relocateConfig}lib/libhdf5.settings
