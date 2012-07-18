### RPM external gsl 1.10
Source: ftp://ftp.gnu.org/gnu/%n/%n-%realversion.tar.gz
Patch0:  gsl-1.10-gcc46

%define keep_archives true

%prep
%setup -n %n-%{realversion}
%patch0 -p1

%build
CFLAGS="-O2" ./configure --prefix=%i --with-pic

make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
rm -f %i/lib/*.la
# Look up documentation online.
%define drop_files %i/share

%post
%{relocateConfig}bin/gsl-config
