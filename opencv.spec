### RPM external opencv 4.3.0
## INITENV +PATH PYTHON27PATH %{i}/${PYTHON_LIB_SITE_PACKAGES}
## INITENV +PATH PYTHON3PATH %{i}/${PYTHON3_LIB_SITE_PACKAGES}
%define tag %{realversion}
%define branch master
%define github_user opencv

Source: git+https://github.com/%{github_user}/opencv.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja
Requires: python python3 py2-numpy py3-numpy libpng libjpeg-turbo libtiff zlib eigen OpenBLAS

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DPYTHON2_EXECUTABLE:FILEPATH="${PYTHON_ROOT}/bin/python" \
    -DPYTHON2_INCLUDE_DIR:PATH="${PYTHON_ROOT}/include/python2.7" \
    -DPYTHON2_LIBRARY:FILEPATH="${PYTHON_ROOT}/lib/libpython2.7.so" \
    -DPYTHON3_EXECUTABLE:FILEPATH="${PYTHON3_ROOT}/bin/python3" \
    -DPYTHON3_INCLUDE_DIR:PATH="${PYTHON3_ROOT}/include/python3.8" \
    -DPYTHON3_LIBRARY:FILEPATH="${PYTHON3_ROOT}/lib/libpython3.8.so" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="${LIBPNG_ROOT};${LIBTIFF_ROOT};${LIBJPEG_TURBO_ROOT};${ZLIB_ROOT};${PYTHON_ROOT};${PYTHON3_ROOT};${PY2_NUMPY_ROOT};${PY3_NUMPY_ROOT};${EIGEN_ROOT};${OPENBLAS_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
