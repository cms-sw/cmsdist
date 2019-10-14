### RPM external fftjet 1.5.0
Source: http://www.hepforge.org/archive/fftjet/%n-%realversion.tar.gz
Requires: fftw3

%define keep_archives true

%prep
%setup -n %n-%realversion

%build
PLATF_CONF_OPTS="--enable-static --disable-shared"
F77="$(which gfortran) -fPIC"
CXX="$(which g++) -fPIC"

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
%get_config_sub ./config.sub
%get_config_guess ./config.guess
chmod +x ./config.{sub,guess}

# Fake the existance of pkg-config on systems which dont have it.
# This is required because it will still check for its existance even
# if you provide DEPS_CFLAGS and DEPS_LIBS.
touch pkg-config ; chmod +x pkg-config
./configure $PLATF_CONF_OPTS --disable-dependency-tracking --enable-threads \
            --prefix=%i F77="$F77" CXX="$CXX" DEPS_CFLAGS=-I$FFTW3_ROOT/include \
            DEPS_LIBS="-L$FFTW3_ROOT/lib -lfftw3" PKG_CONFIG=$PWD/pkg-config
make %makeprocesses

%install
make install
# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig

%post
%{relocateConfig}lib/*.la

