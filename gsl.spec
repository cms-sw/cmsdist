### RPM external gsl 1.8-CMS18
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

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://www.gnu.org/software/gsl/gsl.html"></info>
<lib name=gsl>
<lib name=gslcblas>
<Client>
 <Environment name=GSL_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$GSL_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$GSL_BASE/include"></Environment>
</Client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
