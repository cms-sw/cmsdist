### RPM external xz-bootstrap 5.2.1
Source0: http://tukaani.org/xz/xz-%{realversion}.tar.gz

%prep
%setup -n xz-%{realversion}

%build
# Update for AArch64 support
rm -f ./build-aux/config.{sub,guess}
curl -L -k -s -o ./build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./build-aux/config.{sub,guess}

./configure CFLAGS='-fPIC -D_FILE_OFFSET_BITS=64 -Ofast' --prefix=%{i} --disable-static
make %{makeprocesses}

%install
make %{makeprocesses} install

%define strip_files %{i}/lib
%define drop_files %{i}/share
# bla bla
