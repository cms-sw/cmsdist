### RPM external fftw3 3.2.2
Source: http://www.fftw.org/fftw-%realversion.tar.gz
Patch0: fftw-3.2.2-remove-march-mtune-flags

%prep
%setup -n fftw-%realversion
%patch0 -p1

%build
./configure --with-pic --enable-shared --enable-sse2 --enable-threads \
  --disable-dependency-tracking --disable-fortran --disable-mpi --disable-openmp \
  --prefix=%i
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
