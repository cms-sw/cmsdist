### RPM lcg root 5.99.05
## INITENV +PATH PYTHONPATH %{i}/lib
## INITENV SET ROOTSYS %{i}
%define tag 6b0b92e906b997e0c41d4ea1cc51bcf5aca8ec88
%define branch master
Source: git+http://root.cern.ch/git/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)

#Patch0: root-5.34.02-externals                            in master
#Patch1: root-5.28-00d-roofit-silence-static-printout      can be done via C macro, in rootfit
#Patch2: root-5.34.00-linker-gnu-hash-style
#Patch3: root-5.32.00-detect-arch                          in master
#Patch4: root-5.30.02-fix-gcc46
#Patch5: root-5.30.02-fix-isnan-again
#Patch6: root-5.34.05-cintex-armv7a-port                   not needed anymore

Patch0: root_patch_cms_v03

Requires: gsl libjpg libpng libtiff pcre python fftw3 xz xrootd libxml2 openssl zlib

%if %islinux
Requires: castor dcap
%endif

%if %isdarwin
Requires: freetype
%endif

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
%patch0 -p0

# Delete these (irrelevant) files as the fits appear to confuse rpm on OSX
# (It tries to run install_name_tool on them.)
#rm -fR tutorials/fitsio

sed -ibak -e 's/\/usr\/local/\/no-no-no\/local/g' \
          -e 's/\/opt\/local/\/no-no-no\/local/g' \
          ./configure

%build

mkdir -p %{i}
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

export LZMA=${XZ_ROOT}
export ZLIB=${ZLIB_ROOT}
export LIBJPEG=${LIBJPG_ROOT}
export LIBPNG=${LIBPNG_ROOT}
export LIBTIFF=${LIBTIFF_ROOT}

# Enable debug symbols in ROOT LLVM
export LLVMDEV=1

CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python${PYTHONV}
             --enable-explicitlink 
             --enable-mathmore
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
             --build=debug
             --with-cxx=g++
             --with-cc=gcc
             --with-ld=g++
             --with-f77=gfortran
             --with-gcc-toolchain=${GCC_ROOT}
             --disable-qt
             --disable-qtgsi
             --disable-hdfs
             --disable-oracle ${EXTRA_CONFIG_ARGS}"

#if #isarmv7
#cp ./cint/iosenum/iosenum.linux3 ./cint/iosenum/iosenum.linuxarm3
#endif

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

cat <<\EOF >> MyConfig.mk
CFLAGS+=-D__ROOFIT_NOBANNER
CXXFLAGS+=-D__ROOFIT_NOBANNER
EOF

./configure ${TARGET_PLATF} ${CONFIG_ARGS} ${EXTRA_OPTS}

make %makeprocesses

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
#mkdir -p $ROOTSYS/lib/python
#cp -r cint/reflex/python/genreflex $ROOTSYS/lib/python
# a """ and it thinks is the shebang.
#rm -f %i/tutorials/pyroot/mrt.py

find %{i} -type f -name '*.py' | xargs chmod -x
grep -R -l '#!.*python' %{i} | xargs chmod +x
