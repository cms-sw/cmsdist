### RPM external lhapdf 5.8.5

%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.8.5-32bit-on-64bit-recheck-workaround
Patch1: lhapdf-5.8.5-gzio
Patch2: lhapdf-data-5.8.5-gzio

Requires: zlib

%if "%(echo %cmsos | grep osx >/dev/null && echo true)" == "true"
Requires: gfortran-macosx
%endif
  
%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2

touch src/gzio.inc ; touch src/gzio.F ; touch src/ftn_gzio.c 
%patch1 -p2

cd share/lhapdf/PDFsets
%patch2 -p5

rm -f *gz NNPDF*1000*
gzip -9 *
cd ../../..

%build
# We do everything in install because we need to do it twice.
%install
case %cmsplatf in
  # Looks like configure was generated with an ancient version
  # of autotools which does not work on snow leopard.
  # This seems to fix it. 
  osx*)
    glibtoolize --force --copy
    autoupdate 
    aclocal -Im4
    autoconf
    automake --add-missing
    PLATF_CONF_OPTS="--enable-static --disable-shared"
    PLATF_FC="`which gfortran` -fPIC"
  ;;
  slc*)
    PLATF_CONF_OPTS=""
    PLATF_FC="`which gfortran`"
  ;;
esac

# Remove tests and examples since they have duplicate symbols
# when linking against the archive library.
perl -p -i -e 's|ac_config_files=".ac_config_files examples/Makefile"||' configure
perl -p -i -e 's|ac_config_files=".ac_config_files tests/Makefile"||' configure
rm -rf tests examples

# Configure first with low memory.
./configure --prefix=%i $PLATF_CONF_OPTS --disable-pyext \
            --disable-octave --disable-doxygen \
            --enable-low-memory --with-max-num-pdfsets=1 \
            FC="$PLATF_FC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
perl -p -i -e 's|examples||;s|tests||' Makefile
find . -name Makefile -o -name config.status -exec perl -p -i -e 's|/usr/lib64/lib[cm].a||g' {} \;
make %makeprocesses; make install
mkdir %i/share/lhapdf/PDFsets
mv share/lhapdf/PDFsets/*gz %i/share/lhapdf/PDFsets

# do another install-round for full libs
make distclean
./configure --prefix=%i/full $PLATF_CONF_OPTS \
            --disable-pyext \
            --disable-octave --disable-doxygen\
            FC="$PLATF_FC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
perl -p -i -e 's|examples||;s|tests||' Makefile
find . -name Makefile -o -name config.status -exec perl -p -i -e 's|/usr/lib64/lib[cm].a||g' {} \;
make %makeprocesses; make install
rm -rf %{i}/lib/*.la
