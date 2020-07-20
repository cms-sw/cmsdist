### RPM external hdf5 1.10.6
Source: https://github.com/HDFGroup/hdf5/archive/hdf5-1_10_6.tar.gz
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
