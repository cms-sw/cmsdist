### RPM external gsl 1.10
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz
Patch0:  gsl-1.10-gcc46
Patch1: gsl-1.10-mic

%define keep_archives true

%prep
%setup -n %n-%{realversion}
%patch0 -p1
%if "%mic" == "true"
%patch1 -p1
%endif
%build
case %{cmsplatf} in
   *_mic_* )
    CXX="icpc -fPIC -mmic"  CC="icc -fPIC -mmic" CFLAGS="-O2" ./configure --prefix=%i --with-pic --host=x86_64-k1om-linux
     ;;
   * )
     CFLAGS="-O2" ./configure --prefix=%i --with-pic
     ;;
esac
case $(uname)-$(uname -m) in
  Darwin-i386)
   perl -p -i -e "s|#define HAVE_DARWIN_IEEE_INTERFACE 1|/* option removed */|" config.h;; 
esac

make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
rm -f %i/lib/*.la
# Look up documentation online.
%define drop_files %i/share

%post
%{relocateConfig}bin/gsl-config
