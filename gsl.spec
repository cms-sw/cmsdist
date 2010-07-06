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
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <info url="http://www.gnu.org/software/gsl/gsl.html"/>
    <lib name="gsl"/>
    <lib name="gslcblas"/>
    <client>
      <environment name="GSL_BASE" default="%i"/>
      <environment name="LIBDIR" default="$GSL_BASE/lib"/>
      <environment name="INCLUDE" default="$GSL_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
%{relocateConfig}lib/libgslcblas.la
%{relocateConfig}lib/libgsl.la
