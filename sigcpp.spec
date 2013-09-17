### RPM external sigcpp 2.2.10
%define majorv %(echo %realversion | cut -d. -f1,2) 
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: http://ftp.gnome.org/pub/GNOME/sources/libsigc++/%{majorv}/libsigc++-%{realversion}.tar.bz2

BuildRequires: autotools

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++ -std=c++0x
%endif

%prep
%setup -q -n libsigc++-%{realversion}
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" ./configure --prefix=%{i} --disable-static --host=x86_64-k1om-linux
     ;;
   * )
     ./configure --prefix=%{i} --disable-static CXX="%cms_cxx"
     ;;
esac

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
%define drop_files %i/share
cp %i/lib/sigc++-2.0/include/sigc++config.h %i/include/sigc++-2.0/
