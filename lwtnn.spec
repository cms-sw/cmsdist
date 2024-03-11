### RPM external lwtnn 2.14.1
## INCLUDE cpp-standard


Source: https://github.com/lwtnn/lwtnn/archive/v%{realversion}.tar.gz
Source99: scram-tools.file/tools/eigen/env

Patch0: lwtnn-assert-fix
BuildRequires: ninja cmake
Requires: eigen boost

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build

rm -rf ../build
mkdir ../build
cd ../build
source %{_sourcedir}/env

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_CXX_COMPILER="g++" \
%ifarch x86_64
  -DCMAKE_CXX_FLAGS="-fPIC -DBOOST_DISABLE_ASSERTS  $CMS_EIGEN_CXX_FLAGS -msse3" \
%else
  -DCMAKE_CXX_FLAGS="-fPIC -DBOOST_DISABLE_ASSERTS $CMS_EIGEN_CXX_FLAGS" \
 %endif
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILTIN_BOOST=OFF \
  -DBUILTIN_EIGEN=OFF \
  -DCMAKE_PREFIX_PATH="${EIGEN_ROOT};${BOOST_ROOT}" \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard}

ninja -v %{makeprocesses}

%install

cd ../build

ninja -v %{makeprocesses} install

%post
%{relocateConfig}cmake/lwtnnConfig-targets.cmake
