### RPM external thepeg 1.7.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %i/lib/ThePEG
#Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
#Source: http://projects.hepforge.org/herwig/files/ThePEG-%{realversion}.tar.gz
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/thepeg-%{realversion}-src.tgz
Patch0: thepeg-1.7.0-break-termcap-dependence
Patch1: thepeg-1.7.0-use-dylibs-macosx
Patch2: thepeg-1.6.1-lhapdf-env
Patch3: thepeg-1.6.1-gcc46
Patch4: thepeg-1.7.0-configure
Patch5: thepeg-1.7.0-gcc46
Requires: lhapdf
Requires: gsl
Requires: hepmc
Requires: zlib
# FIXME: rivet?
%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
case %cmsos in 
  osx*)
%patch1 -p1
  ;;
esac
%patch2 -p2
%patch3 -p2
%patch4 -p1
%patch5 -p1

%build
# Build as static only on new architectures.
case %cmsplatf in 
  slc5*_*_gcc4[01234]*) 
    CXX="`which c++`"
    CC="`which gcc`"    
    PLATF_CONF_OPTS="--enable-shared --disable-static"
    LIBGFORTRAN=`gfortran --print-file-name=libgfortran.so` 
  ;;
  *) perl -p -i -e 's|libLHAPDF[.]so|libLHAPDF.a|g' configure 
    CXX="`which c++` -fPIC"
    CC="`which gcc` -fPIC"
    PLATF_CONF_OPTS="--enable-shared --disable-static"
    LIBGFORTRAN="`gfortran --print-file-name=libgfortran.so`"
  ;;
esac

case %cmsplatf in
  osx*) LIBGFORTRAN="`gfortran --print-file-name=libgfortran.a`" ;;
esac

case %cmsplatf in
  osx*_*_gcc4[0-5]*) ;;
  osx*_*_gcc*) LIBQUADMATH="-lquadmath" ;;
esac

./configure $PLATF_CONF_OPTS \
            --with-LHAPDF=$LHAPDF_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT --with-zlib=$ZLIB_ROOT \
            --without-javagui --prefix=%i \
            --disable-readline CXX="$CXX" CC="$CC" \
            LIBS="-L$LHAPDF_ROOT/lib -lLHAPDF $LIBGFORTRAN -lz $LIBQUADMATH"
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl
cd %i/lib/ThePEG
for item in LesHouches.so ; do
  [ -e lib$item ] || ln -s $item lib$item
done
rm -rf %i/lib/*.la
