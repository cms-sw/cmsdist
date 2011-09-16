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
find %i/lib -type f -perm -a+x -exec strip {} \;

# Don't need archive libraries.
rm -f %i/lib/*.{l,}a

# Look up documentation online.
rm -rf %i/share

%post
%{relocateConfig}lib/*.la
