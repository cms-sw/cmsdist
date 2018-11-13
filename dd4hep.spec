### RPM external dd4hep v01-08x

%define tag a710edf3953bacb6a6be9e1d591df55794cf07c2
%define branch cms/master/c627ab2
%define github_user cms-externals

Source: git+https://github.com/%{github_user}/DD4hep.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: cmake

Requires: root boost clhep xerces-c

%prep

%setup -n %{n}-%{realversion}

%build

rm -rf ../build
mkdir ../build
cd ../build

export BOOST_ROOT
cmake -DCMAKE_INSTALL_PREFIX="%{i}" \
      -DBoost_NO_BOOST_CMAKE=ON \
      -DCMAKE_PREFIX_PATH=${CLHEP_ROOT} \
      -DDD4HEP_USE_XERCESC=ON \
      -DXERCESC_ROOT_DIR=${XERCES_C_ROOT} \
      -DDD4HEP_USE_PYROOT=ON \
      -DCMAKE_CXX_STANDARD=17 \
      -DCMAKE_BUILD_TYPE=Release \
      ../%{n}-%{realversion}

make %{makeprocesses} VERBOSE=1

%install

cd ../build
make install

%post
%{relocateConfig}*.cmake
%{relocateConfig}bin/*.sh
%{relocateConfig}bin/*.csh
