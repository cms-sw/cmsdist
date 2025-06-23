### RPM external hdf5 1.8.17
Source: https://support.hdfgroup.org/ftp/HDF5/current/src/%{n}-%{realversion}.tar.bz2
BuildRequires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
rm -f ./bin/config.{sub,guess}
%get_config_sub ./bin/config.sub
%get_config_guess ./bin/config.guess
chmod +x ./bin/config.{sub,guess}
./configure --enable-shared --enable-cxx --with-zlib=${ZLIB_ROOT} --prefix %{i}
make %{makeprocesses} VERBOSE=1

%install
make install

%post
