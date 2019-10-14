### RPM external davix 0.7.3

%define tag %(echo R_%{realversion} | tr . _)
%define branch master
%define github_user cern-it-sdc-id
Source0: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define soext so
%ifarch darwin
%define soext dylib
%endif

BuildRequires: cmake gmake git
Requires: libxml2 libuuid
%prep
%setup -n %{n}-%{realversion}

%build
# need this until we have the submodule recursive option
cd ../ ; rm -rf %{n}-%{realversion}
git clone https://github.com/%{github_user}/%{n}.git %{n}-%{realversion} ; cd %{n}-%{realversion} ; git checkout tags/%{tag}
git submodule update --recursive --init
mkdir build ; cd build

cmake -DCMAKE_INSTALL_PREFIX="%{i}" \
 -DLIBXML2_INCLUDE_DIR="${LIBXML2_ROOT}/include/libxml2" \
 -DLIBXML2_LIBRARY="${LIBXML2_ROOT}/lib/libxml2.%{soext}" \
 -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
 -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
 ../

make VERBOSE=1 %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}lib64/pkgconfig/davix.pc
