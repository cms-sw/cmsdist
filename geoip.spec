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
%define strip_files %i/lib

# Look up documentation online.
%define drop_files %i/share/man
