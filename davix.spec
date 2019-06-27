### RPM external davix 0.6.7

%define tag %(echo R_%{realversion} | tr . _)
%define branch master
%define github_user cern-it-sdc-id
Source0: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define soext so
%if %isdarwin
%define soext dylib
%endif

BuildRequires: cmake gmake 
Requires: openssl libxml2 libuuid
%prep
%setup -n %{n}-%{realversion}

%build
mkdir build ; cd build
cmake -DCMAKE_INSTALL_PREFIX="%{i}" \
 -DLIBXML2_INCLUDE_DIR="${LIBXML2_ROOT}/include/libxml2" \
 -DLIBXML2_LIBRARIES="${LIBXML2_ROOT}/lib/libxml2.%{soext}" \
 -DUUID_INCLUDE_DIR="${LIBUUID_ROOT}/include" \
 -DUUID_LIBRARY="${LIBUUID_ROOT}/lib64/libuuid.%{soext}" \
 -DOPENSSL_ROOT_DIR="${OPENSSL_ROOT}" \
 ../

make VERBOSE=1 %{makeprocesses}

%install
cd build
make install

%post
%{relocateConfig}lib64/pkgconfig/davix.pc
# bla bla
