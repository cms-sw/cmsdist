### RPM external ittnotify 3.28.4

Source: https://github.com/intel/ittapi/archive/refs/tags/v%{realversion}.tar.gz
BuildRequires: cmake
%define keep_archives true

%prep
%setup -q -n ittapi-%{realversion}

%build
cmake -DCMAKE_INSTALL_PREFIX="%{i}" .
 
make %{makeprocesses} VERBOSE=1 all

%install
make install

