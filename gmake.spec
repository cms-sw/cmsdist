### RPM external gmake 3.81-CMS18
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz

%prep
%setup -n make-%{realversion}

%build
./configure --prefix=%i

make %makeprocesses

%install
make install
# Put in the symlink
ln -s %i/make %/gmake

# SCRAM ToolBox toolfile (still to add)
