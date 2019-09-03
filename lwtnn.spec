### RPM external lwtnn 2.10

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
  -DCMAKE_PREFIX_PATH="${EIGEN_ROOT};${BOOST_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install

cd ../build

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
