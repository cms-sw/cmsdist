### RPM lcg root 5.34.17
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define tag 369426d4ef79
%define branch cms/v5-34-17
%define github_user cms-sw
Source: git+https://github.com/%github_user/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isonline %(case %{cmsplatf} in (*onl_*_*) echo 1 ;; (*) echo 0 ;; esac)
%define isnotonline %(case %{cmsplatf} in (*onl_*_*) echo 0 ;; (*) echo 1 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
%if "%mic" == "true"
Requires: icc
Requires: freetype
Patch90: root-5.34.09-mic
Patch91: root-5-genreflex
Patch92: root-5.34.09-mic-postconfig
%endif

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

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

# Delete these (irrelevant) files as the fits appear to confuse rpm on OSX
# (It tries to run install_name_tool on them.)
rm -fR tutorials/fitsio

# Block use of /opt/local, /usr/local.
perl -p -i -e 's{/(usr|opt)/local}{/no-no-no/local}g' configure

%if "%mic" == "true"
%patch90 -p1
%patch91 -p1
%endif

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

%if "%mic" == "true"
CONFIG_ARGS="$CONFIG_ARGS --enable-xml  --with-xml-incdir=${LIBXML2_ROOT}/include/libxml2 --with-xml-libdir=${LIBXML2_ROOT}/lib
             --with-cxx=icc --with-cc=icc --with-f77=ifort --with-ld=icc
             --disable-x11 --disable-xft --disable-rfio --disable-builtin_afterimage"
sed -ibak 's/-mmic/-mmic -std=c++0x/g' config/Makefile.linuxx8664k1omicc
%endif

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
                            --disable-builtin_afterimage
                            --disable-cocoa
                            --enable-x11"
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
make %{makeprocesses}
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
