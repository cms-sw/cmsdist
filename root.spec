### RPM lcg root 5.27.06b
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
%define ismac %(case %cmsplatf in osx*%closingbrace echo true;; *%closingbrace echo false;; esac)

Patch0: root-5.27-06-externals
Patch1: root-5.27-04-CINT-maxlongline-maxtypedef
Patch2: root-5.22-00a-roofit-silence-static-printout
Patch3: root-5.22-00d-linker-gnu-hash-style
Patch4: root-5.22-00d-TBranchElement-dropped-data-member
Patch5: root-5.27-06-fireworks9
Patch6: root-5.27-06b-gdb-backtrace
Patch7: root-5.27-06-tmva-DecisionTreeNode
Patch8: root-5.27-06b-r36567
Patch9: root-5.27-06b-r36572
Patch10: root-5.27-06b-r36707
Patch11: root-5.27-06b-r36594
Patch12: root-5.27-06b-tmva-MethodBase-initvar
Patch13: root-5.27-06b-r37582-tmva
Patch14: root-5.27-06b-r37405
Patch15: root-5.27-06b-r37556
Patch16: root-5.27-06-fireworks10
Patch17: root-5.27-06-TTreeClonerTopLevel
Patch18: root-5.27-06b-r37947
Patch19: root-5.27-06b-TTreeCache-r37950-r37919-r37917-r37916-r37906
Patch20: root-5.27-06b-extra-math-for-roofit-5.28.00
Patch21: root-5.27-06b-TEfficiency-backport-from-5.28.00
Patch22: root-5.27-06b-histfactory-bits-from-5.28.00
Patch23: root-5.27-06b-r37210
Patch24: root-5.27-06b-r38023
Patch25: root-5.27-06b-r36708
Patch26: root-5.27-06b-r38126-r38156
Patch27: root-5.27-06b-r38210
Patch28: root-5.27-06b-r38248-r38252-r38259-r38264-r38265-r38267
Patch29: root-5.27-06b-gcc46
Patch30: root-5.27-06b-r38325
Patch31: root-5.27-06b-tmva-MethodANNBase-uninitialized-var-fix
Patch32: root-5.27-06b-r36196-r36698
Patch33: root-5.27-06-fireworks11
Patch34: root-5.27-06b-r38369
Patch35: root-5.27-06b-r39055
Patch36: root-5.27.06b-r39155
Patch37: root-5.27.06b-r38057
Patch38: root-5.27-06b-tbasket_revised_buffers_v4_cms527
Patch39: root-5.27.06b-r39139
Patch40: root-5.28-00d-r39525
Patch41: root-5.28-00d-fix-tsystem-load-macosx
Patch42: root-5.27.06b-longBranchName
Patch43: root-5.27.06b-r45588

%define cpu %(echo %cmsplatf | cut -d_ -f2)

Requires: gccxml gsl libjpg libpng libtiff libungif pcre python fftw3

%if "%ismac" != "true"
Requires: castor dcap
%endif

%if "%online" != "true"
Requires: openssl zlib xrootd
%endif

%if "%ismac" == "true"
Requires: gfortran-macosx
%endif

%prep
%setup -n root
%patch0 -p1
%patch1 -p1
%patch2 -p1
# patch3 is OS version dependent, see below
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p0
%patch18 -p1
%patch19 -p0
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p2
%patch38 -p1
%patch39 -p0
%patch42 -p1
%patch43 -p0

# Since it is needed only to fix inline visibility issues,
# we apply it only for gcc 4.5.1 and later.
case %cmsplatf in
  slc5_*_gcc4[01234]*) ;;
  *)
%patch40 -p1
  ;;
esac

%patch41 -p1

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
case %cmsplatf in
  slc5_* | slc5onl_* )
%patch3 -p1
  ;;
esac

# Delete these (irrelevant) files as the fits appear to confuse rpm on OSX
# (It tries to run install_name_tool on them.)
rm -fR tutorials/fitsio

%build

mkdir -p %i
export LIBJPG_ROOT
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

%if "%online" == "true"
# Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="--with-f77=/usr
             --disable-odbc --disable-astiff"
%else
export LIBPNG_ROOT ZLIB_ROOT LIBTIFF_ROOT LIBUNGIF_ROOT
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib"
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
             --enable-fftw3
             --with-fftw3-incdir=${FFTW3_ROOT}/include
             --with-fftw3-libdir=${FFTW3_ROOT}/lib
             --disable-ldap
             --disable-krb5
             --with-xrootd=${XROOTD_ROOT}
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-mysql
             --disable-qt --disable-qtgsi
             --disable-oracle ${EXTRA_CONFIG_ARGS}"

case %cmsos in
  slc*_amd64)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-rfio-libdir=${CASTOR_ROOT}/lib --with-rfio-incdir=${CASTOR_ROOT}/include/shift --with-castor-libdir=${CASTOR_ROOT}/lib --with-castor-incdir=${CASTOR_ROOT}/include/shift ;; 
  slc*_ia32)
    ./configure linux  $CONFIG_ARGS --with-rfio-libdir=${CASTOR_ROOT}/lib --with-rfio-incdir=${CASTOR_ROOT}/include/shift --with-castor-libdir=${CASTOR_ROOT}/lib --with-castor-incdir=${CASTOR_ROOT}/include/shift ;;
  osx*)
    case %cmsplatf in
    *_ia32_* ) 
      comparch=i386 
      macconfig=macosx
      ;; 
    *_amd64_* )
      comparch=x86_64
      macconfig=macosx64
      ;; 
    * ) 
      comparch=ppc 
      macconfig=macosx
      ;;
    esac
    export CC=`which gcc` CXX=`which g++`
    ./configure $arch $CONFIG_ARGS --with-cc="$CC" --with-cxx="$CXX" --disable-rfio --disable-builtin_afterimage ;;
  slc*_ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

makeopts="%makeprocesses"

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
# This file confuses rpm's find-requires because it starts with
# a """ and it thinks is the shebang.
rm -f %i/tutorials/pyroot/mrt.py


 
