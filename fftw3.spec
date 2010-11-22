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

%post
%{relocateConfig}lib/pkgconfig/fftw3.pc
%{relocateConfig}lib/*.la
