### RPM external lwtnn 2.13
## INCLUDE cpp-standard

Source: https://github.com/lwtnn/lwtnn/archive/v%{realversion}.tar.gz
BuildRequires: ninja cmake
Requires: eigen boost

%prep
%setup -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_CXX_COMPILER="g++" \
  -DCMAKE_CXX_FLAGS="-fPIC" \
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
