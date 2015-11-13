### RPM external davix 0.4.0

%define tag %(echo R_%{realversion} | tr . _)
%define branch master
%define github_user cern-it-sdc-id
Source0: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake gmake 
Requires: openssl libxml2 boost
%prep
%setup -n %{n}-%{realversion}

%build
mkdir build ; cd build
cmake -DCMAKE_INSTALL_PREFIX="%{i}" \
 -DLIBXML2_INCLUDE_DIR="${LIBXML2_ROOT}/include/libxml2" \
 -DLIBXML2_LIBRARIES="${LIBXML2_ROOT}/lib/libxml2.so" \
 -DBoost_NO_SYSTEM_PATHS:BOOL=TRUE \
 -DBOOST_ROOT:PATH="${BOOST_ROOT}" \
 ../

make VERBOSE=1 %{makeprocesses}

%install
cd build
make install
