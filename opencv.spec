### RPM external opencv 4.3.0

%define tag 01b2c5a77ca6dbef3baef24ebc0a5984579231d9
%define branch master
%define github_user opencv

Source: git+https://github.com/%{github_user}/opencv.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake ninja
Requires: python libpng libjpeg-turbo libtiff zlib

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -GNinja \
    -DCMAKE_INSTALL_PREFIX="%{i}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="${LIBPNG_ROOT};${LIBTIFF_ROOT};${LIBJPEG_TURBO_ROOT};${ZLIB_ROOT};${PYTHON_ROOT}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build
ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install
