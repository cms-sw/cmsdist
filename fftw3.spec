### RPM external fftw3 3.2.2
Source: http://www.fftw.org/fftw-%realversion.tar.gz

%prep
%setup -n fftw-%realversion

%build
# This matches the configure options used to build FFTW3.1.2 for SL5
./configure --enable-shared --disable-dependency-tracking --enable-threads --prefix=%i
make %makeprocesses

%install
make install

# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Remove documentation. 
%define drop_files %i/share
rm -rf %i/lib/*.la
