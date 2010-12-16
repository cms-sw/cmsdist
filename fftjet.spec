### RPM external fftjet 1.3.1
Source: http://www.hepforge.org/archive/fftjet/%n-%realversion.tar.gz
Requires: fftw3

%prep
%setup -n %n-%realversion

%build
export DEPS_CFLAGS=-I$FFTW3_ROOT/include
export DEPS_LIBS="-L$FFTW3_ROOT/lib -lfftw3"
export F77=gfortran
./configure --enable-shared --disable-dependency-tracking --enable-threads --prefix=%i
make %makeprocesses

%install
make install

%post
%{relocateConfig}lib/pkgconfig/fftjet.pc
%{relocateConfig}lib/*.la
