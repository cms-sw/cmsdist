### RPM external sigcpp 2.0.17
Requires: gcc-wrapper
%define majorv %(echo %v | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{v}.tar.gz

%prep
%setup -q -n libsigc++-%{v}
./configure  --prefix=%{i} 

%build
## IMPORT gcc-wrapper
make %makeprocesses 
%install
make install
cp %i/lib/sigc++-%{majorv}/include/sigc++config.h %i/include/sigc++-%{majorv}/
