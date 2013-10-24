### RPM lcg roofit 5.99.04
## INITENV +PATH PYTHONPATH %{i}/lib
## INITENV SET ROOTSYS %{i}
%define tag a098127973bc003c21667c466e2be10d1d0e0486
%define branch master
Source: git+http://root.cern.ch/git/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define isarmv7 %(case %{cmsplatf} in (*armv7*) echo 1 ;; (*) echo 0 ;; esac)

#atch0: root6-externals
#atch1: root6-cling-opts

#Patch0: root-5.34.02-externals
#Patch1: root-5.28-00d-roofit-silence-static-printout
#Patch2: root-5.34.00-linker-gnu-hash-style
#Patch3: root-5.32.00-detect-arch
#Patch4: root-5.30.02-fix-gcc46
#Patch5: root-5.30.02-fix-isnan-again
#Patch6: root-5.34.05-cintex-armv7a-port

Requires: root

#equires: gsl libjpg libpng libtiff pcre python fftw3 xz xrootd libxml2 openssl zlib

#if %islinux
#equires: castor dcap
#endif

#if %isdarwin
#equires: freetype
#endif

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}
#patch0 -p1
#patch1 -p1

sed -ibak -e 's/\/usr\/local/\/no-no-no\/local/g' \
          -e 's/\/opt\/local/\/no-no-no\/local/g' \
          ./configure

%build
mkdir -p %{i}
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

#export LZMA=${XZ_ROOT}
#export ZLIB=${ZLIB_ROOT}
#export LIBJPEG=${LIBJPEG_ROOT}
#export LIBPNG=${LIBPNG_ROOT}
#export LIBTIFF=${LIBTIFF_ROOT}

# Enable debug symbols in ROOT LLVM
export LLVMDEV=1

CONFIG_ARGS="--minimal
             --enable-roofit
             --enable-xml
             --enable-c++11
             --build=debug
             --disable-rpath
             --with-cxx=${GCC_ROOT}/bin/g++
             --with-cc=${GCC_ROOT}/bin/gcc
             --with-ld=${GCC_ROOT}/bin/g++
             --with-f77=${GCC_ROOT}/bin/gfortran
             --with-gcc-toolchain=${GCC_ROOT}"

TARGET_PLATF=

%if %islinux
  TARGET_PLATF=linuxx8664gcc
%endif

%if %isdarwin
  TARGET_PLATF=macosx64
%endif

%if %isarmv7
  TARGET_PLATF=linuxarm
%endif

cat <<\EOF >> MyConfig.mk
CFLAGS+=-D__ROOFIT_NOBANNER
CXXFLAGS+=-D__ROOFIT_NOBANNER
EOF

./configure ${TARGET_PLATF} ${CONFIG_ARGS}

make %{makeprocesses}

%install
mkdir -p %{i}/{lib,bin,include,tutorials}
cp ./lib/{libHistFactory*,libRooFitCore*,libRooFit*,libRooStats*} %{i}/lib
cp ./bin/{prepareHistFactory,hist2workspace} %{i}/bin
rsync -av --exclude='*LinkDef*.h' ./roofit/{roofit,roofitcore,roostats,histfactory}/inc/ %{i}/include/
