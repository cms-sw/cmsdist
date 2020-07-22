### RPM external hdf5 1.10.6
Source: git+https://github.com/HDFGroup/%{n}.git?obj=master/5b9cf732caab9daa6ed1e00f2df4f5a792340196&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
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
