### RPM external triton-inference-common 2.11.0
%define branch main
%define github_user triton-inference-server
%define tag_2_11_0 249232758855cc764c78a12964c2a5c09c388d87
%define keep_archives true

Source: git+https://github.com/%{github_user}/common.git?obj=%{branch}/%{tag_2_11_0}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake
Requires: protobuf grpc

%prep

%setup -n %{n}-%{realversion}

%build

# locations of CMakeLists.txt
PROJ_DIR=../%{n}-%{realversion}
CML_TOP=${PROJ_DIR}/CMakeLists.txt
CML_PRB=${PROJ_DIR}/protobuf/CMakeLists.txt

# remove rapidjson dependence
sed -i '/RapidJSON CONFIG REQUIRED/,+1d;' ${CML_TOP}
sed -i '/JSON utilities/,+17d' ${CML_TOP}
sed -i '/triton-common-json/d' ${CML_TOP}
# remove python dependence
sed -i '/Python REQUIRED COMPONENTS Interpreter/,+10d;' ${CML_PRB}
# change flag due to bug in gcc10 https://gcc.gnu.org/bugzilla/show_bug.cgi?id=95148
if [[ `gcc --version | head -1 | cut -d' ' -f3 | cut -d. -f1,2,3 | tr -d .` -gt 1000 ]] ; then 
    sed -i -e "s|Werror|Wtype-limits|g" ${CML_PRB}
fi

rm -rf ../build
mkdir ../build
cd ../build

cmake ${PROJ_DIR} \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DCMAKE_BUILD_TYPE=Release \
    -DTRITON_COMMON_ENABLE_PROTOBUF=ON \
    -DTRITON_COMMON_ENABLE_GRPC=ON \
    -DCMAKE_CXX_FLAGS="-Wno-error" \

make %{makeprocesses}
# for some reason these aren't built in the default target
make %{makeprocesses} proto-library
make %{makeprocesses} grpc-service-library
make install

# copy static libs by hand
mkdir -p %i/lib/
for lib in *.a; do
  cp ${lib} %i/lib/
done

%install
