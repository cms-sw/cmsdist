### RPM external xz-bootstrap 5.2.4
Source0: http://tukaani.org/xz/xz-%{realversion}.tar.gz

%prep
%setup -n xz-%{realversion}

%build
# Update for AArch64 support
rm -f ./build-aux/config.{sub,guess}
%get_config_guess ./build-aux/config.guess
%get_config_sub   ./build-aux/config.sub
chmod +x ./build-aux/config.{sub,guess}

./configure CFLAGS='-fPIC -D_FILE_OFFSET_BITS=64 -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
