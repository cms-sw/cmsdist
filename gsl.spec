### RPM external gsl 1.8-XXXX
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz

%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i
case $(uname)-$(uname -m) in
  Darwin-i386)
   perl -p -i -e "s|#define HAVE_DARWIN_IEEE_INTERFACE 1|/* option removed */|" config.h;; 
esac

make %makeprocesses
# mysqlpp.spec
#
