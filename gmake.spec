### RPM external gmake 3.81
# We will call it "gmake", but gnu calls it "make"
Source: ftp://ftp.gnu.org/gnu/make/make-%realversion.tar.gz
Patch0: gmake-3.81-expand

%prep
%setup -n make-%{realversion}
%patch0 -p1

%build
./configure --prefix=%i

make %makeprocesses

%install
make install
# Put in the symlink
cd %{i}/bin
ln -sf make gmake

%define drop_files %i/{man,info}
