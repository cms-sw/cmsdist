### RPM external protobuf 3.5.2
## INITENV SETV PROTOBUF_SOURCE %{source0}
## INITENV SETV PROTOBUF_STRIP_PREFIX %{source_prefix}
#============= IMPORTANT NOTE ========================#
# When changing the version of protobuf, remember to regenerate protobuf objects in CMSSW
# current recipe for this is:
# cmsenv
# git cms-addpkg DQMServices/Core
# cd $CMSSW_BASE/src
# protoc --cpp_out=. DQMServices/Core/src/ROOTFilePB.proto
#######################################################

#These are needed by Tensorflow sources
#NOTE: Never apply any patch in the spec file, this way tensorflow gets the exact same sources
%define source0 https://github.com/google/protobuf/archive/v%{realversion}.tar.gz
%define source_prefix %{n}-%{realversion}

Source: %{source0}
Requires: zlib
BuildRequires: autotools

%prep
%setup -n %{source_prefix}

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
# bla bla
