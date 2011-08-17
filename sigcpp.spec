### RPM external sigcpp 2.2.3
%define majorv %(echo %realversion | cut -d. -f1,2) 
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.gz
Patch0: sigcpp-2.2.3-gcc46

%prep
%setup -q -n libsigc++-%{realversion}
case %gccver in
  4.6.*)
%patch0 -p1
  ;;
esac
./configure --prefix=%{i} --disable-static

%build
make %makeprocesses 
%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig
# Read documentation online.
rm -rf %i/share
cp %i/lib/sigc++-2.0/include/sigc++config.h %i/include/sigc++-2.0/
