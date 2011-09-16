### RPM external gsl 1.10
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz
Patch0:  gsl-1.10-gcc46
%prep
%setup -n %n-%{realversion}
%patch0 -p1

%build
CFLAGS="-O2" ./configure --prefix=%i --with-pic
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
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/share

%post
%{relocateConfig}lib/libgslcblas.la
%{relocateConfig}lib/libgsl.la
%{relocateConfig}bin/gsl-config
