### RPM external adns 1.4
Source: http://www.chiark.greenend.org.uk/~ian/adns/ftp/adns-%realversion.tar.gz
Patch: adns-osx-build

%prep
%setup -n %n-%realversion
%ifos darwin
%patch
autoreconf -i
%endif

%build
./configure --prefix=%i
make %makeprocesses

%install
make install

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a
