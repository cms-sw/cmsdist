### RPM lcg root 5.34.07
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define tag %(echo v%{realversion} | tr . -)
%define branch %(echo %{realversion} | sed 's/\\.[0-9]*$/.00/;s/^/v/;s/$/-patches/g;s/\\./-/g')
Source: git+http://root.cern.ch/git/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
%define ismac %(case %cmsplatf in (osx*) echo true;; (*) echo false;; esac)

Patch0: root-5.34.02-externals
Patch1: root-5.28-00d-roofit-silence-static-printout
Patch2: root-5.34.00-linker-gnu-hash-style
Patch3: root-5.32.00-detect-arch
Patch4: root-5.30.02-fix-gcc46
Patch5: root-5.30.02-fix-isnan-again
Patch6: root-5.34.07-fix-fatal-removal-in-branch-names

%define cpu %(echo %cmsplatf | cut -d_ -f2)

Requires: gccxml gsl libjpg libpng libtiff pcre python fftw3 xz xrootd libxml2 openssl

%if "%ismac" != "true"
Requires: castor dcap
%endif

%if "%online" != "true"
Requires: zlib
%endif

%define keep_archives true
%if "%(case %cmsplatf in (osx*_*_gcc421) echo true ;; (*) echo false ;; esac)" == "true"
Requires: gfortran-macosx
%endif

%if "%(case %cmsplatf in (osx*) echo true ;; (*) echo false ;; esac)" == "true"
Requires: freetype
%endif

%prep
%setup -n root-%realversion
%patch0 -p1
%patch1 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
case %cmsplatf in
  slc[56]_* | slc5onl_* )
%patch2 -p1
  ;;
esac

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
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
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

case %cmsos in
  slc*)
    ./configure linuxx8664gcc $CONFIG_ARGS \
                  --with-rfio-libdir=${CASTOR_ROOT}/lib \
                  --with-rfio-incdir=${CASTOR_ROOT}/include/shift \
                  --with-castor-libdir=${CASTOR_ROOT}/lib \
                  --with-castor-incdir=${CASTOR_ROOT}/include/shift ;; 
  osx*)
    comparch=x86_64
    macconfig=macosx64
    ./configure $arch $CONFIG_ARGS --disable-rfio --disable-builtin_afterimage ;;
  slc*_ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

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
