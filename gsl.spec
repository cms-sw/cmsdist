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

%post
%{relocateConfig}lib/libgslcblas.la
%{relocateConfig}lib/libgsl.la
