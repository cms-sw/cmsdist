### RPM external sigcpp 2.0.17
%define majorv 2.0
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{v}.tar.gz

%prep
%setup -q -n libsigc++-%{v}
./configure  --prefix=%{i} 

%build
make 

%install
make install

