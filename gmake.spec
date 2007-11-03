### RPM external gmake 3.81-CMS18
# We will call it "gmake", but gnu calls it "make"
Source: ftp://ftp.gnu.org/gnu/make/make-%realversion.tar.gz
Patch1: gmake-3.81-expand

%prep
%setup -n make-%{realversion}
%patch1 -p0

%build
./configure --prefix=%i

make %makeprocesses

%install
make install
# Put in the symlink
cd %{i}/bin
ln -s make gmake

# SCRAM ToolBox toolfile (still to add)
