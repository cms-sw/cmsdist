### RPM external lhapdf 5.8.5

%define realversion %(echo %v | cut -d- -f1)
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Patch0: lhapdf-5.8.5-32bit-on-64bit-recheck-workaround
Patch1: lhapdf-5.8.5-gzio
Patch2: lhapdf-data-5.8.5-gzio

Requires: zlib
%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
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
cat <<\EOF > ../compress.mk
FILES=$(addsuffix .gz,$(wildcard *))
all: ${FILES}
%.gz: %
	gzip -9 $<
EOF

make -j 4 -f ../compress.mk all
cd ../../..

%build
# We do everything in install because we need to do it twice.
%install
# Regenerate the configure and makefiles since we modified 
# the Makefile.am to include the gzip stuff.
LIBTOOLIZE=`which glibtoolize || which libtoolize`
$LIBTOOLIZE --force --copy
autoupdate
aclocal -I m4
autoconf
automake --add-missing

# Only old platform can be build using shared librari 
case %cmsplatf in 
  slc5_*_gcc4[01234]*) 
    FC="`which gfortran`"
    CXX="`which c++`"
    CC="`which gcc`"
  ;;
  *) 
    PLATF_CONF_OPTS="--enable-static --disable-shared" 
    FC="`which gfortran` -fPIC"
    CXX="`which c++` -fPIC"
    CC="`which gcc` -fPIC"
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
            FC="$FC" CXX="$CXX" CC="$CC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
perl -p -i -e 's|examples||;s|tests||' Makefile
find . -name Makefile -o -name config.status -exec perl -p -i -e 's|/usr/lib64/lib[cm].a||g' {} \;
make %makeprocesses; make install
mkdir %i/share/lhapdf/PDFsets
mv share/lhapdf/PDFsets/*gz %i/share/lhapdf/PDFsets
pushd %i/share/lhapdf/PDFsets
  for x in `ls *.gz`; do
    ln -sf $x `echo $x | sed -e's|\.gz$||'`
  done
popd

# do another install-round for full libs
make distclean
./configure --prefix=%i/full $PLATF_CONF_OPTS \
            --disable-pyext \
            --disable-octave --disable-doxygen\
            FC="$FC" CXX="$CXX" CC="$CC" \
            CPPFLAGS="-I ${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib -lz"
perl -p -i -e 's|examples||;s|tests||' Makefile
find . -name Makefile -o -name config.status -exec perl -p -i -e 's|/usr/lib64/lib[cm].a||g' {} \;
make %makeprocesses; make install
rm -rf %{i}/lib/*.la
