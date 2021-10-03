### RPM external log4cplus 2.0.5
%define relver %(echo %{realversion} | tr '.' '_')
Source: https://github.com/%{n}/%{n}/releases/download/REL_2_0_5/%{n}-%{realversion}.tar.gz
BuildRequires: cmake gmake
%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
rm -rf ../build; mkdir ../build ; cd ../build
cmake ../%{n}-%{realversion} -DCMAKE_INSTALL_PREFIX=%{i} \
  -DBUILD_SHARED_LIBS:BOOL=OFF \
  -DLOG4CPLUS_BUILD_TESTING=OFF \
  -DLOG4CPLUS_BUILD_LOGGINGSERVER=OFF

make %{makeprocesses} VERBOSE=1

%install
cd ../build
make install
