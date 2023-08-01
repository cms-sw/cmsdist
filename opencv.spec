### RPM external opencv 4.7.0
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define tag %{realversion}
%define branch master
%define github_user opencv

Source0: git+https://github.com/%{github_user}/opencv.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja
Requires: python3 py3-numpy libpng libjpeg-turbo libtiff zlib eigen OpenBLAS

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_CXX_STANDARD=17 \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DWITH_EIGEN=ON \
    -DBUILD_EXAMPLES=OFF \
    -DWITH_QT=OFF \
    -DWITH_GTK=OFF \
    -DPYTHON3_EXECUTABLE:FILEPATH="${PYTHON3_ROOT}/bin/python3" \
    -DPYTHON3_INCLUDE_DIR:PATH="${PYTHON3_ROOT}/include/python%{cms_python3_major_minor_version}" \
    -DPYTHON3_LIBRARY:FILEPATH="${PYTHON3_ROOT}/lib/libpython%{cms_python3_major_minor_version}.so" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="${LIBPNG_ROOT};${LIBTIFF_ROOT};${LIBJPEG_TURBO_ROOT};${ZLIB_ROOT};${PYTHON3_ROOT};${PY2_NUMPY_ROOT};${PY3_NUMPY_ROOT};${EIGEN_ROOT};${OPENBLAS_ROOT}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install
