### RPM external protobuf 3.11.3
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
BuildRequires: cmake ninja

%prep
%setup -n %{source_prefix}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion}/cmake \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_CXX_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_C_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_SHARED_LINKER_FLAGS="-L${ZLIB_ROOT}/lib" \
    -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install

cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
rm -rf %{i}/lib/pkgconfig
