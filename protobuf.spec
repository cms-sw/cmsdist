### RPM external protobuf 3.21.9
## INCLUDE cpp-standard
#============= IMPORTANT NOTE ========================#
# When changing the version of protobuf, remember to regenerate protobuf objects in CMSSW
# current recipe for this is:
# cmsenv
# git cms-addpkg DQMServices/Core
# cd $CMSSW_BASE/src
# protoc --cpp_out=. DQMServices/Core/src/ROOTFilePB.proto
#######################################################

%define keep_archives true

Source: https://github.com/protocolbuffers/protobuf/archive/v%{realversion}.zip
Requires: zlib
BuildRequires: cmake ninja

%prep
%setup -n %{n}-%{realversion}
# Make sure the default c++sdt stand is c++11
grep -q 'CMAKE_CXX_STANDARD  *11' CMakeLists.txt
sed -i -e 's|CMAKE_CXX_STANDARD  *11|CMAKE_CXX_STANDARD %{cms_cxx_standard}|' CMakeLists.txt
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
 
