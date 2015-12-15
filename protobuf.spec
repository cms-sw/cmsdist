### RPM external protobuf 2.4.1
Source: http://protobuf.googlecode.com/files/%{n}-%{realversion}.tar.bz2
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

rm -f ./gtest/build-aux/config.{sub,guess}
curl -L -k -s -o ./gtest/build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./gtest/build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./gtest/build-aux/config.{sub,guess}

./configure --prefix %{i} \
    --disable-static \
    --disable-dependency-tracking \
    CXXFLAGS="-I${ZLIB_ROOT}/include" \
    CFLAGS="-I${ZLIB_ROOT}/include" \
    LDFLAGS="-L${ZLIB_ROOT}/lib"
make %{makeprocesses}

%install
make install
rm -rf %{i}/lib/pkgconfig
