### RPM external libarchive-bootstrap 3.1.2
Source0: http://www.libarchive.org/downloads/libarchive-%{realversion}.tar.gz

Requires: zlib-bootstrap xz-bootstrap bz2lib-bootstrap

%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}

%prep  
%setup -n libarchive-%{realversion}

# Update config.{guess,sub} scripts
rm -f %{_tmppath}/config.{sub,guess}
curl -L -k -s -o %{_tmppath}/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
curl -L -k -s -o %{_tmppath}/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
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
  CPPFLAGS="-I${ZLIB_BOOTSTRAP_ROOT}/include -I${XZ_BOOTSTRAP_ROOT}/include -I${BZ2LIB_BOOTSTRAP_ROOT}/include" \
  LDFLAGS="-L${ZLIB_BOOTSTRAP_ROOT}/lib -L${XZ_BOOTSTRAP_ROOT}/lib -L${BZ2LIB_BOOTSTRAP_ROOT}/lib"

make %{makeprocesses}

%install
make install

find %{i}/lib -type f -name '*.la' -delete
