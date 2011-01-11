### RPM external gsl 1.10
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
CFLAGS="-O2" ./configure --prefix=%i --with-pic
case $(uname)-$(uname -m) in
  Darwin-i386)
   perl -p -i -e "s|#define HAVE_DARWIN_IEEE_INTERFACE 1|/* option removed */|" config.h;; 
esac

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
%post
%{relocateConfig}lib/libgslcblas.la
%{relocateConfig}lib/libgsl.la
%{relocateConfig}bin/gsl-config
