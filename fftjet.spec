### RPM external fftjet 1.3.1
Source: http://www.hepforge.org/archive/fftjet/%n-%realversion.tar.gz
Requires: fftw3
%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -n %n-%realversion

%build
# Fake the existance of pkg-config on systems which dont have it.
# This is required because it will still check for its existance even
# if you provide DEPS_CFLAGS and DEPS_LIBS.
touch pkg-config ; chmod +x pkg-config
./configure --enable-shared --disable-dependency-tracking --enable-threads \
            --prefix=%i F77=`which gfortran` DEPS_CFLAGS=-I$FFTW3_ROOT/include \
            DEPS_LIBS="-L$FFTW3_ROOT/lib -lfftw3" PKG_CONFIG=$PWD/pkg-config
make %makeprocesses

%install
make install

%post
%{relocateConfig}lib/pkgconfig/fftjet.pc
%{relocateConfig}lib/*.la
