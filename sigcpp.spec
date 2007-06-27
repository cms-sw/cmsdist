### RPM external sigcpp 2.0.17-CMS3
%define majorv %(echo %realversion | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.gz

%prep
%setup -q -n libsigc++-%{realversion}
./configure --prefix=%{i} 

%build
make %makeprocesses 
%install
make install
cp %i/lib/sigc++-%{majorv}/include/sigc++config.h %i/include/sigc++-%{majorv}/
