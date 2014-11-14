### RPM external yaml-cpp 0.5.1
Source: http://yaml-cpp.googlecode.com/files/%{n}-%{realversion}.tar.gz

BuildRequires: cmake

Requires: boost

%prep
%setup -n %{n}-%{realversion}

 
%build
cmake . \
  -DCMAKE_INSTALL_PREFIX:PATH="%{i}" \
  -DBUILD_SHARED_LIBS=YES \
  -DBoost_NO_SYSTEM_PATHS:BOOL=TRUE \
  -DBoost_NO_BOOST_CMAKE:BOOL=TRUE \
  -DBoost_ADDITIONAL_VERSIONS="1.57.0" \
  -DBOOST_ROOT:PATH=${BOOST_ROOT} \
  -DCMAKE_SKIP_RPATH=YES \
  -DSKIP_INSTALL_FILES=1

make %{makeprocesses} VERBOSE=1

%install
make install

%post
