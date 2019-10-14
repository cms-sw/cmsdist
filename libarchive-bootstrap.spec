### RPM external libarchive-bootstrap 3.3.2
Source0: http://www.libarchive.org/downloads/libarchive-%{realversion}.tar.gz

Requires: xz-bootstrap

%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}

%prep  
%setup -n libarchive-%{realversion}

# Update config.{guess,sub} scripts
rm -f %{_tmppath}/config.{sub,guess}
%get_config_guess %{_tmppath}/config.guess
%get_config_sub %{_tmppath}/config.sub
for CONFIG_GUESS_FILE in $(find . -name 'config.guess')
do
  rm -f $CONFIG_GUESS_FILE
  cp %{_tmppath}/config.guess $CONFIG_GUESS_FILE
  chmod +x $CONFIG_GUESS_FILE
done
for CONFIG_SUB_FILE in $(find . -name 'config.sub')
do
  rm -f $CONFIG_SUB_FILE
  cp %{_tmppath}/config.sub $CONFIG_SUB_FILE
  chmod +x $CONFIG_SUB_FILE
done

%build
./configure \
  --prefix=%{i} \
  --disable-silent-rules \
  --disable-dependency-tracking \
  --disable-rpath \
  --disable-bsdtar \
  --disable-bsdcpio \
  --enable-static \
  --disable-shared \
  --without-lzmadec \
  --without-iconv \
  --without-lzo2 \
  --without-nettle \
  --without-openssl \
  --without-xml2 \
  --without-expat \
  CPPFLAGS="-I${XZ_BOOTSTRAP_ROOT}/include" \
  LDFLAGS="-L${XZ_BOOTSTRAP_ROOT}/lib"

make %{makeprocesses}

%install
make install

find %{i}/lib -type f -name '*.la' -delete
