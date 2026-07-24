### RPM external protobuf 6.31.1
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
Requires: zlib abseil-cpp
BuildRequires: cmake ninja

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -G Ninja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -Dprotobuf_BUILD_TESTS=OFF \
    -Dprotobuf_BUILD_SHARED_LIBS=ON \
    -Dutf8_range_ENABLE_INSTALL=ON \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_CXX_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_C_FLAGS="-I${ZLIB_ROOT}/include" \
    -DCMAKE_SHARED_LINKER_FLAGS="-L${ZLIB_ROOT}/lib" \
    -DCMAKE_PREFIX_PATH="${ABSEIL_CPP_ROOT};${ZLIB_ROOT}"

ninja -v %{makeprocesses}

%install

cd ../build
ninja -v %{makeprocesses} install
mkdir -p %{i}/include/python/google/protobuf
cp ../%{n}-%{realversion}/python/google/protobuf/*.h %{i}/include/python/google/protobuf/
rm -rf %{i}/lib/pkgconfig
