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
# This applies both old and new fixes, probably the gcc4 ones can go (to check) 
case %gccver in
  4.*)
    # Switch to gfortran
    perl -p -i -e 's|^export F77\=g77|export F77=gfortran|' .scripts/platform_functions
    perl -p -i -e 's| -Wno-globals||' configure
  ;;
esac
%patch0 -p2

touch src/gzio.inc ; touch src/gzio.F ; touch src/ftn_gzio.c 

%patch1 -p2

cd share/lhapdf/PDFsets
%patch2 -p5
rm -f *gz NNPDF*1000*
gzip -9 *
cd ../../..

%build
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
  ;;
esac
./configure --disable-pyext --disable-octave --disable-doxygen --prefix=%i --enable-low-memory --with-max-num-pdfsets=1 F77=gfortran CPPFLAGS="-I ${LIBZLIB}/include" LDFLAGS="-L${LIBZLIB}/lib -lz" 

perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make 

%install
make install

mkdir %i/share/lhapdf/PDFsets
mv share/lhapdf/PDFsets/*gz %i/share/lhapdf/PDFsets

# do another install-round for full libs
make distclean
%define fulllibpath %(echo %i"/full")
%define fullname %(echo %n"full")
./configure --disable-pyext --disable-octave --disable-doxygen --prefix=%fulllibpath F77=gfortran CPPFLAGS="-I ${LIBZLIB}/include" LDFLAGS="-L${LIBZLIB}/lib -lz" 
perl -p -i -e 's|/usr/lib64/libm.a||g' config.status
perl -p -i -e 's|/usr/lib64/libc.a||g' config.status
perl -p -i -e 's|/usr/lib64/libm.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
perl -p -i -e 's|/usr/lib64/libc.a||g' Makefile */Makefile */*/Makefile */*/*/Makefile
make
make install

%post
%{relocateConfig}lib/libLHAPDF.la
%{relocateConfig}lib/libLHAPDFWrap.la
