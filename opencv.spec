### RPM external opencv 4.5.1
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define tag %{realversion}
%define branch master
%define github_user opencv

Source0: git+https://github.com/%{github_user}/opencv.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Source1: https://patch-diff.githubusercontent.com/raw/opencv/opencv/pull/19692.patch
BuildRequires: cmake ninja
Requires: python3 py3-numpy libpng libjpeg-turbo libtiff zlib eigen OpenBLAS

%prep
%setup -n %{n}-%{realversion}
patch -p1 < %{_sourcedir}/19692.patch

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DWITH_EIGEN=ON \
    -DPYTHON3_EXECUTABLE:FILEPATH="${PYTHON3_ROOT}/bin/python3" \
    -DPYTHON3_INCLUDE_DIR:PATH="${PYTHON3_ROOT}/include/python3.9" \
    -DPYTHON3_LIBRARY:FILEPATH="${PYTHON3_ROOT}/lib/libpython3.9.so" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="${LIBPNG_ROOT};${LIBTIFF_ROOT};${LIBJPEG_TURBO_ROOT};${ZLIB_ROOT};${PYTHON3_ROOT};${PY2_NUMPY_ROOT};${PY3_NUMPY_ROOT};${EIGEN_ROOT};${OPENBLAS_ROOT}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install
