### RPM external ittnotify 16.06.18

Source: https://github.com/01org/IntelSEAPI/archive/%{realversion}.tar.gz
BuildRequires: cmake
%define keep_archives true

%prep
%setup -q -n IntelSEAPI-%{realversion}

%build
cmake -DCMAKE_INSTALL_PREFIX="%{i}" -DARCH_64=1 ittnotify
 
make %{makeprocesses} VERBOSE=1 all

%install
mkdir %{i}/lib %{i}/include
cp libittnotify64.a  %{i}/lib/libittnotify.a
cp ittnotify/include/ittnotify.h %{i}/include

# bla bla
