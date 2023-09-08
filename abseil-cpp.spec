### RPM external abseil-cpp 20230125.4
## INCLUDE cpp-standard

%define tag c2435f8342c2d0ed8101cb43adfd605fdc52dca2
%define branch lts_2023_01_25
%define github_user abseil
Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz

BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
    -DCMAKE_INSTALL_PREFIX=%{i} \
    -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
    -DCMAKE_INSTALL_LIBDIR=lib \
    -DBUILD_TESTING=OFF \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_BUILD_TYPE=Release

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%define strip_files %i/lib
%define drop_files %i/lib/pkgconfig
