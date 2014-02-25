### RPM external c-ares 1.10.0
Source: http://c-ares.haxx.se/download/%n-%realversion.tar.gz
Provides: libcares.2.so()(64bit)   
%prep
%setup -n %n-%{realversion}

%build
./configure --prefix=%i 
make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Read documentation online.
%define drop_files %i/share

%post
