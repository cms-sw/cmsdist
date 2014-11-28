### RPM external thepeg 1.9.2p1
## INITENV +PATH LD_LIBRARY_PATH %i/lib/ThePEG
## INITENV +PATH DYLD_LIBRARY_PATH %i/lib/ThePEG
Source: http://service-spi.web.cern.ch/service-spi/external/MCGenerators/distribution/%{n}/%{n}-%{realversion}-src.tgz
Patch0: thepeg-1.7.0-break-termcap-dependence
Patch1: thepeg-1.7.0-use-dylibs-macosx
Patch6: thepeg-1.9.2-fix-bogus-ZLIB-HOME
Patch7: thepeg-1.9.2p1-fix-LHAPDF-get-index
Requires: lhapdf
Requires: gsl
Requires: hepmc
Requires: zlib
# FIXME: rivet?
%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%if "%{?cms_cxx:set}" != "set"
%define cms_cxx c++
%endif

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -O2 -std=c++0x
%endif

%prep
%setup -q -n %{n}/%{realversion}
%patch0 -p2
#The patch for mac below is disabled, it does not work. If it is still needed, it is to be redone.
case %cmsos in 
  osx*)
#%patch1 -p1
  ;;
esac
%patch6 -p1
%patch7 -p0

# Trick make not to re-run aclocal, autoconf, automake, autoscan, etc.
find . -exec touch -m -t 201201010000 {} \;

%build
# Build as static only on new architectures.
case %cmsplatf in 
  slc5*_*_gcc4[01234]*) 
    CXX="`which %cms_cxx`"
    CC="`which gcc`"    
    PLATF_CONF_OPTS="--enable-shared --disable-static"
    LIBGFORTRAN=`gfortran --print-file-name=libgfortran.so` 
  ;;
  *) perl -p -i -e 's|libLHAPDF[.]so|libLHAPDF.a|g' configure 
    CXX="`which %cms_cxx` -fPIC"
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
            --disable-silent-rules \
            --with-LHAPDF=$LHAPDF_ROOT \
            --with-hepmc=$HEPMC_ROOT \
            --with-gsl=$GSL_ROOT --with-zlib=$ZLIB_ROOT \
            --without-javagui --prefix=%i \
            --disable-readline CXX="$CXX" CC="$CC" CXXFLAGS="%cms_cxxflags" \
            LIBS="$LIBGFORTRAN -lz $LIBQUADMATH"
make

%install

make install

cd %i/lib/ThePEG
for item in LesHouches.so ; do
  [ -e lib$item ] || ln -s $item lib$item
done
find %i/lib -name '*.la' -exec rm -f {} \;

%post
%{relocateConfig}lib/ThePEG/Makefile.common
%{relocateConfig}lib/ThePEG/Makefile
%{relocateConfig}lib/ThePEG/ThePEGDefaults.rpo
%{relocateConfig}lib/ThePEG/ThePEGDefaults-1.9.2.rpo
