### RPM lcg root 5.22.00d
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Patch0: root-5.18-00-libpng 
Patch1: root-5.22-00d-CINT-maxlongline-maxtypedef
Patch2: root-5.22-00-TMVA-shut-the-hell-up-for-once
Patch3: root-5.22-00a-TMVA-shut-the-hell-up-again
Patch4: root-5.22-00d-fireworks-graf3d-gui
Patch5: root-5.22-00a-roofit-silence-static-printout
Patch6: root-5.22-00a-TMVA-just-shut-the-hell-up
Patch7: root-5.22-00a-th1
Patch8: root-5.22-00d-makelib-ldl
Patch9: root-5.22-00a-fireworks1
Patch10: root-5.22-00a-gcc44 
Patch11: root-5.22-00a-fireworks2
Patch12: root-5.22-00a-fireworks3
Patch13: root-5.22-00a-gcc43-array-bounds-dictionary-workaround
Patch14: root-5.22-00a-fireworks4
Patch15: root-5.22-00d-fireworks5
Patch16: root-5.22-00d-genreflex_python26_popen3
Patch17: root-5.22-00d-fireworks6
Patch18: root-5.22-00d-linker-gnu-hash-style
Patch19: root-5.22-00d-TFile-version3-Init 
Patch20: root-5.22-00d-cint-namespace
Patch21: root-5.22-00d-fireworks7
Patch22: root-5.22-00d-TMath-Vavilov
Patch23: root-5.22-00d-TBranchElement-dropped-data-member
Patch24: root-5.22-00d-fireworks8

%define cpu %(echo %cmsplatf | cut -d_ -f2)

Requires: gccxml gsl castor libjpg dcap pcre python

%if "%online" != "true"
Requires: qt openssl libpng zlib libungif xrootd
%else
%define skiplibtiff true
%endif

%if "%cpu" == "amd64"
%define skiplibtiff true
%endif

%if "%skiplibtiff" != "true"
Requires: libtiff
%endif

%prep
%setup -n root
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# patch10 is compiler version dependent, see below
%patch11 -p1
%patch12 -p1
# patch13 is compiler version dependent, see below

# work around patch issue...
rm graf3d/gl/src/gl2ps.c
%patch14 -p1
#work around patch issues in patch14(?)
rm graf3d/eve/inc/TEveLegoOverlay.h.orig
rm graf3d/eve/src/TEveLegoOverlay.cxx
rm graf3d/gl/inc/gl2ps.h.orig
rm graf3d/gl/src/gl2ps.c.orig
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1

case %gccver in
  4.3.*)
%patch13 -p1
  ;;
  4.4.*)
%patch10 -p1
  ;;
esac

# The following patch can only be applied on SLC5 or later (extra linker 
# options only available with the SLC5 binutils)
case %cmsplatf in
  slc5_* | slc5onl_* )
%patch18 -p1
  ;;
esac

%build

mkdir -p %i
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

%if "%online" == "true"
# Use system qt. Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="--with-f77=/usr
             --disable-xrootd
             --disable-odbc
             --disable-qt --disable-qtgsi"
%else
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}
             --with-xrootd=$XROOTD_ROOT
             --enable-qt --with-qt-libdir=${QT_ROOT}/lib --with-qt-incdir=${QT_ROOT}/include 
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
	     --enable-qtgsi"
%endif

CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python${PYTHONV}
             --enable-explicitlink 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --disable-ldap
             --disable-krb5
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-mysql
             --disable-xml ${EXTRA_CONFIG_ARGS}"

case $(uname)-$(uname -m) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift --disable-astiff;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift;;
  Darwin*)
    case %cmsplatf in
    *_ia32_* ) 
      comparch=i386 ;;
    *_amd64_* )
      comparch=x86_64 ;;
    * ) 
      comparch=ppc ;;
    esac
    export CC="gcc -arch $comparch" CXX="g++ -arch $comparch"
    ./configure macosx $CONFIG_ARGS --with-cc="$CC" --with-cxx="$CXX" --disable-rfio --disable-builtin_afterimage ;;
  Linux-ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

case %cmsplatf in
  osx*)
   makeopts=
  ;;
  *)
   makeopts="%makeprocesses"
  ;;
esac
 
make $makeopts 
make cintdlls

%install
# Override installers if we are using GNU fileutils cp.  On OS X
# ROOT's INSTALL is defined to "cp -pPR", which only works with
# the system cp (/bin/cp).  If you have fileutils on fink, you
# lose.  Check which one is getting picked up and select syntax
# accordingly.  (FIXME: do we need to check that -P is accepted?)
if (cp --help | grep -e '-P.*--parents') >/dev/null 2>&1; then
  cp="cp -dpR"
else
  cp="cp -pPR"
fi

export ROOTSYS=%i
make INSTALL="$cp" INSTALLDATA="$cp" install
mkdir -p $ROOTSYS/lib/python
cp -r cint/reflex/python/genreflex $ROOTSYS/lib/python
