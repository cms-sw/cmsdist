### RPM external geoip 1.4.6
Source: http://geolite.maxmind.com/download/geoip/api/c/GeoIP-%realversion.tar.gz

%prep
%setup -n GeoIP-%realversion

%build
./configure --prefix=%i
make %makeprocesses

%install
make install

# Strip libraries, we are not going to debug them.
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/share/man
