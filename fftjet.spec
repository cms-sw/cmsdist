### RPM external fftjet 1.3.1
Source: http://www.hepforge.org/archive/fftjet/%n-%realversion.tar.gz
Requires: fftw3
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -n %n-%realversion

%build
./configure --enable-shared --disable-dependency-tracking --enable-threads \
            --prefix=%i F77=`which gfortran` DEPS_CFLAGS=-I$FFTW3_ROOT/include \
            DEPS_LIBS="-L$FFTW3_ROOT/lib -lfftw3"
make %makeprocesses

%install
make install

%post
%{relocateConfig}lib/pkgconfig/fftjet.pc
%{relocateConfig}lib/*.la
