### RPM external protobuf 3.21.9
#============= IMPORTANT NOTE ========================#
# When changing the version of protobuf, remember to regenerate protobuf objects in CMSSW
# current recipe for this is:
# cmsenv
# git cms-addpkg DQMServices/Core
# cd $CMSSW_BASE/src
# protoc --cpp_out=. DQMServices/Core/src/ROOTFilePB.proto
#######################################################

%define keep_archives true

Source: https://github.com/protocolbuffers/protobuf/archive/v3.21.9.zip
#Patch0: protobuf-3.15-gcc10
#Patch1: protobuf-std_iterator-8741
Requires: zlib
BuildRequires: cmake ninja

%prep
%setup -n %{n}-%{realversion}
#%patch0 -p1
#%patch1 -p1
#sed -i -e 's|CMAKE_CXX_STANDARD  *11|CMAKE_CXX_STANDARD 17|' cmake/CMakeLists.txt
%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -Dutf8_range_ENABLE_INSTALL=ON \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_CXX_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_C_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_SHARED_LINKER_FLAGS="-L${ZLIB_ROOT}/lib" \
    -DCMAKE_PREFIX_PATH="${ZLIB_ROOT}"

ninja -v %{makeprocesses}

%install

cd ../build
ninja -v %{makeprocesses} install
rm -rf %{i}/lib/pkgconfig
 # rebuild #
