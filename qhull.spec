### RPM external qhull 8.0.2
Source: https://github.com/qhull/qhull/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: cmake gmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
 -DBUILD_STATIC_LIBS:BOOL=OFF \
 -DBUILD_SHARED_LIBS:BOOL=ON \
 -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_INSTALL_PREFIX:STRING=%{i}

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install
