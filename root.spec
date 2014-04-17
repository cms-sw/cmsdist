### RPM lcg root 5.34.17
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define tag %(echo v%{realversion} | tr . -)
%define branch %(echo %{realversion} | sed 's/\\.[0-9]*$/.00/;s/^/v/;s/$/-patches/g;s/\\./-/g')
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
%endif
Source: git+http://root.cern.ch/git/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isonline %(case %{cmsplatf} in (*onl_*_*) echo 1 ;; (*) echo 0 ;; esac)
%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)

Patch0: root-5.34.02-externals
Patch1: root-5.28-00d-roofit-silence-static-printout
Patch2: root-5.34.00-linker-gnu-hash-style
Patch3: root-5.32.00-detect-arch
Patch4: root-5.30.02-fix-gcc46
Patch5: root-5.30.02-fix-isnan-again
Patch6: root-5.34.05-cintex-armv7a-port
Patch7: 0001-Use-meta-data-mutex-for-the-proxy-initialization
Patch8: 0002-Fix-thread-safety-of-TThread-TThread-Long_t-id
Patch9: 0003-Reduce-lifetime-of-lock-in-TFile-TFile-to-avoid-lock
Patch10: 0004-Reduce-lock-lifetime-in-TCollection-GarbageCollect
Patch11: 0005-Remove-unnecessary-global-variable-and-lock
Patch12: 0006-Fix-thread-safety-of-TGenCollectionProxy-s-iterator-
Patch13: root-5.34.13-ExpandMaxTypedef_02
Patch14: https://github.com/Dr15Jones/root/commit/97b24fb57166a105d3912ee0ac0c3bc27af54afa.patch
Patch15: https://github.com/Dr15Jones/root/commit/e04ab19e95c14665a2b5e464f30c54d226b490e0.patch
Patch16: https://github.com/Dr15Jones/root/commit/386c35244cd8901c243bbc8dd10ac1643e44b589.patch
Patch17: https://github.com/Dr15Jones/root/commit/285552177b57fa931d4e2f6e67ea3cb0414c736b.patch
Patch90: root-5.34.09-mic
Patch91: root-5-genreflex
Patch92: root-5.34.09-mic-postconfig
Patch18: root-5.34.17-linuxarm-cxx11

Requires: gccxml gsl libjpg libpng libtiff pcre python fftw3 xz xrootd libxml2 openssl

%if %islinux
%if "%mic" != "true"
Requires: castor dcap
%endif
%endif

%if %isnotonline
Requires: zlib
%endif

%if %isdarwin
Requires: freetype
%endif
%if "%mic" == "true"
Requires: freetype
%endif

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%if %isarmv7
%patch6 -p1
%endif

%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p0
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
%if %islinux
%patch2 -p1
%endif
%if "%mic" == "true"
%patch90 -p1
%patch91 -p1
%endif

# Delete these (irrelevant) files as the fits appear to confuse rpm on OSX
# (It tries to run install_name_tool on them.)
rm -fR tutorials/fitsio

# Block use of /opt/local, /usr/local.
perl -p -i -e 's{/(usr|opt)/local}{/no-no-no/local}g' configure

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
%if "%mic" != "true"
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}"
%else
export OPENSSL_ROOT FREETYPE_ROOT PCRE_ROOT
export ROOTCINT_MIC_ROOT
%endif
%endif
LZMA=${XZ_ROOT}
export LZMA
%if "%mic" == "true"
CONFIG_ARGS="--enable-table --enable-genvector --enable-tmva
             --enable-xml  --with-xml-incdir=${LIBXML2_ROOT}/include/libxml2 --with-xml-libdir=${LIBXML2_ROOT}/lib
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
             --disable-builtin-lzma
             --enable-fftw3
             --with-fftw3-incdir=${FFTW3_ROOT}/include
             --with-fftw3-libdir=${FFTW3_ROOT}/lib
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
             --disable-ldap
             --disable-krb5
             --with-xrootd=${XROOTD_ROOT}
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --disable-pgsql
             --disable-mysql
             --enable-c++11
             --with-cxx=icc
             --with-cc=icc
             --with-f77=ifort
             --disable-x11 --disable-xft
             --disable-qt --disable-qtgsi
             --with-cint-maxstruct=36000
             --with-cint-maxtypedef=36000
             --with-cint-longline=4096
             --disable-hdfs
             --disable-oracle ${EXTRA_CONFIG_ARGS}
             --disable-rfio --disable-builtin_afterimage"
%else
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
             --disable-builtin-lzma
             --enable-fftw3
             --with-fftw3-incdir=${FFTW3_ROOT}/include
             --with-fftw3-libdir=${FFTW3_ROOT}/lib
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
             --disable-ldap
             --disable-krb5
             --with-xrootd=${XROOTD_ROOT}
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --disable-pgsql
             --disable-mysql
             --enable-c++11
             --with-cxx=g++
             --with-cc=gcc
             --with-ld=g++
             --disable-qt --disable-qtgsi
             --with-cint-maxstruct=36000
             --with-cint-maxtypedef=36000
             --with-cint-longline=4096
             --disable-hdfs
             --disable-oracle ${EXTRA_CONFIG_ARGS}"
%endif

# Add support for GCC 4.6
sed -ibak 's/\-std=c++11/-std=c++0x/g' \
  configure \
  Makefile \
  config/Makefile.macosx64 \
  config/Makefile.macosx \
  config/Makefile.linux \
  config/root-config.in \
  config/Makefile.linuxx8664gcc \
  config/Makefile.linuxx8664k1omicc

EXTRA_OPTS=
TARGET_PLATF=

%if %islinux
  TARGET_PLATF=linuxx8664gcc
  EXTRA_OPTS="${EXTRA_OPTS} --with-rfio-libdir=${CASTOR_ROOT}/lib 
                            --with-rfio-incdir=${CASTOR_ROOT}/include/shift
                            --with-castor-libdir=${CASTOR_ROOT}/lib
                            --with-castor-incdir=${CASTOR_ROOT}/include/shift
                            --with-dcap-libdir=${DCAP_ROOT}/lib
                            --with-dcap-incdir=${DCAP_ROOT}/include"
%endif

%if %isdarwin
  TARGET_PLATF=macosx64
  EXTRA_OPTS="${EXTRA_OPTS} --disable-rfio
                            --disable-builtin_afterimage"
%endif

%if %isarmv7
  TARGET_PLATF=linuxarm
%endif

%if "%mic" == "true"
TARGET_PLATF=linuxx8664k1omicc
EXTRA_OPTS="--with-thread-libdir=`pwd`/thrd"
mkdir thrd; ln -s /lib64/libpthread.so.0 thrd/libpthread.so
./configure ${TARGET_PLATF} ${CONFIG_ARGS} ${EXTRA_OPTS}
cat %_sourcedir/root-5.34.09-mic-postconfig | patch -s -p1 --fuzz=0
%else
./configure ${TARGET_PLATF} ${CONFIG_ARGS} ${EXTRA_OPTS}
%endif

%if "%mic" == "true"
F77OPT="-mmic" CFLAGS="-Dthread_local=" make -k %makeprocesses  || true
F77OPT="-mmic" CFLAGS="-Dthread_local=" make %makeprocesses
%else
make %makeprocesses CXX="g++ -DOS_OBJECT_USE_OBJC=0 -DDLL_DECL=" CC="gcc -DOS_OBJECT_USE_OBJC=0 -DDLL_DECL="
%endif

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
rm -f %i/tutorials/pyroot/mrt.py %i/cint/test/testall.cxx
%if "%mic" == "true"
mkdir -p $ROOTSYS/rootcint/bin $ROOTSYS/rootcint/lib
cp buildtools/bin/rlibmap $ROOTSYS/bin/
cp buildtools/bin/rootcint $ROOTSYS/rootcint/bin/
cp buildtools/lib/libCint.so $ROOTSYS/rootcint/lib/
cp -r buildtools/cint $ROOTSYS/rootcint/
%endif

%post
%{relocateConfig}bin/root-config
%{relocateConfig}include/RConfigOptions.h
%{relocateConfig}include/compiledata.h
%{relocateConfig}cint/cint/lib/G__c_ipc.d
%{relocateConfig}cint/cint/lib/G__c_stdfunc.d
%{relocateConfig}cint/cint/lib/G__c_posix.d
%{relocateConfig}lib/python/genreflex/gccxmlpath.py
