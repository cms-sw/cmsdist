### RPM external thepeg 1.9.2p1
## INITENV +PATH LD_LIBRARY_PATH %{i}/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %{i}/lib/ThePEG

%define tag 41e9a26f5ca9659e30e9c27e4dc86e65ecd4a4bd
%define branch cms/v%realversion

Source: git+https://github.com/cms-externals/thepeg.git?obj=%{branch}/%{tag}&export=thepeg-%{realversion}-%{tag}&module=thepeg-%realversion-%{tag}&output=/thepeg-%{realversion}-%{tag}.tgz
Requires: lhapdf
Requires: gsl
Requires: hepmc
Requires: zlib
BuildRequires: autotools
# FIXME: rivet?
%define keep_archives true

%prep
%setup -q -n thepeg-%{realversion}-%{tag}

# Regenerate build scripts
autoreconf -fiv

%build
CXX="$(which g++) -fPIC"
CC="$(which gcc) -fPIC"
PLATF_CONF_OPTS="--enable-shared --disable-static"

case %{cmsplatf} in
  osx*)
    LIBQUADMATH="-lquadmath"
    ;;
esac

# Update to detect aarch64 and ppc64le
rm -f ./Config/config.{sub,guess}
curl -L -k -s -o ./Config/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./Config/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./Config/config.{sub,guess}

./configure $PLATF_CONF_OPTS \
            --disable-silent-rules \
            --with-LHAPDF=$LHAPDF_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT --with-zlib=$ZLIB_ROOT \
            --without-javagui --prefix=%{i} \
            --disable-readline CXX="$CXX" CC="$CC" \
            LIBS="-lz $LIBQUADMATH"

make %{makeprocesses}

%install
make install
find %{i}/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}lib/ThePEG/Makefile.common
%{relocateConfig}lib/ThePEG/Makefile
%{relocateConfig}lib/ThePEG/ThePEGDefaults.rpo
%{relocateConfig}lib/ThePEG/ThePEGDefaults-1.9.2.rpo
