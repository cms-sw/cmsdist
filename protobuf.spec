### RPM external protobuf 3.4.0
Source: https://github.com/google/protobuf/archive/v%{realversion}.tar.gz
Requires: zlib

#
# When changing the version of protobuf, remember to regenerate protobuf objects in CMSSW
# current recipe for this is:
# cmsenv
# git cms-addpkg DQMServices/Core
# cd $CMSSW_BASE/src
# protoc --cpp_out=. DQMServices/Core/src/ROOTFilePB.proto

%prep
%setup -n %{n}-%{realversion}

%build
./autogen.sh
# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}


rm -f ./gmock/gtest/build-aux/config.{sub,guess}
curl -L -k -s -o ./gmock/gtest/build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./gmock/gtest/build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./gmock/gtest/build-aux/config.{sub,guess}

rm -f ./gmock/build-aux/config.{sub,guess}
curl -L -k -s -o ./gmock/build-aux/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./gmock/build-aux/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./gmock/build-aux/config.{sub,guess}
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
