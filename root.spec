### RPM lcg root 5.34.09
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define tag %(echo v%{realversion} | tr . -)
%define branch %(echo %{realversion} | sed 's/\\.[0-9]*$/.00/;s/^/v/;s/$/-patches/g;s/\\./-/g')
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
Patch7: root-5.34.09-ROOT-5437

Requires: gccxml gsl libjpg libpng libtiff pcre python fftw3 xz xrootd libxml2 openssl

%if %islinux
Requires: castor dcap
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
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch7 -p1

%if %isarmv7
%patch6 -p1
%endif

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
%if %islinux
%patch2 -p1
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
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}"
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

# Add support for GCC 4.6
sed -ibak 's/\-std=c++11/-std=c++0x/g' \
  configure \
  Makefile \
  config/Makefile.macosx64 \
  config/Makefile.macosx \
  config/Makefile.linux \
  config/root-config.in \
  config/Makefile.linuxx8664gcc 

%if %isarmv7
cp ./cint/iosenum/iosenum.linux3 ./cint/iosenum/iosenum.linuxarm3
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
                            --disable-builtin_afterimage"
%endif

%if %isarmv7
  TARGET_PLATF=linuxarm
%endif

./configure ${TARGET_PLATF} ${CONFIG_ARGS} ${EXTRA_OPTS}

make %makeprocesses CXX="g++ -DOS_OBJECT_USE_OBJC=0 -DDLL_DECL=" CC="gcc -DOS_OBJECT_USE_OBJC=0 -DDLL_DECL="

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

%post
%{relocateConfig}bin/root-config
%{relocateConfig}include/RConfigOptions.h
%{relocateConfig}include/compiledata.h
%{relocateConfig}cint/cint/lib/G__c_ipc.d
%{relocateConfig}cint/cint/lib/G__c_stdfunc.d
%{relocateConfig}cint/cint/lib/G__c_posix.d
%{relocateConfig}lib/python/genreflex/gccxmlpath.py
