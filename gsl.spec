### RPM external gsl 1.8
Requires: gcc-wrapper
Source: ftp://ftp.gnu.org/gnu/%n/%n-%v.tar.gz
%build
## IMPORT gcc-wrapper

./configure --prefix=%i
case $(uname)-$(uname -m) in
  Darwin-i386)
   perl -p -i -e "s|#define HAVE_DARWIN_IEEE_INTERFACE 1|/* option removed */|" config.h;; 
esac

make %makeprocesses
# mysqlpp.spec
#
