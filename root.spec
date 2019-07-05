### RPM lcg root 6.18.00
## INITENV +PATH PYTHON27PATH %{i}/lib
## INITENV +PATH PYTHON3PATH %{i}/lib
## INITENV SET ROOTSYS %{i}
%define tag aafd101474844016c6878266bc89844ff45fb9b4
%define branch cms/v6-18-00-patches/48aabf4
%define github_user cms-sw
Source: git+https://github.com/%{github_user}/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

BuildRequires: cmake ninja

Requires: gsl libjpeg-turbo libpng libtiff giflib pcre python fftw3 xz xrootd libxml2 openssl zlib davix tbb OpenBLAS py2-numpy lz4

%if %islinux
Requires: dcap
%endif

%if %isdarwin
Requires: freetype
%endif

%define soext so
%if %isdarwin
%define soext dylib
%endif

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)
export CFLAGS=-D__ROOFIT_NOBANNER
export CXXFLAGS=-D__ROOFIT_NOBANNER

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_C_COMPILER=gcc \
  -DCMAKE_CXX_COMPILER=g++ \
  -DCMAKE_Fortran_COMPILER=gfortran \
  -DCMAKE_LINKER=ld \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -Droot7=ON \
  -Dfail-on-missing=ON \
  -Dgnuinstall=OFF \
  -Droofit=ON \
  -Dvdt=OFF \
  -Dhdfs=OFF \
  -Dqt=OFF \
  -Dqtgsi=OFF \
  -Dpgsql=OFF \
  -Dsqlite=OFF \
  -Dmysql=OFF \
  -Doracle=OFF \
  -Dldap=OFF \
  -Dkrb5=OFF \
  -Dftgl=OFF \
  -Dfftw3=ON \
  -Dtbb=ON \
  -Dimt=ON \
  -DFFTW_INCLUDE_DIR="${FFTW3_ROOT}/include" \
  -DFFTW_LIBRARY="${FFTW3_ROOT}/lib/libfftw3.%{soext}" \
  -Dminuit2=ON \
  -Dmathmore=ON \
  -Dexplicitlink=ON \
  -Dtable=OFF \
  -Dbuiltin_tbb=OFF \
  -Dbuiltin_pcre=OFF \
  -Dbuiltin_freetype=OFF \
  -Dbuiltin_zlib=OFF \
  -Dbuiltin_lzma=OFF \
  -Dbuiltin_gsl=OFF \
  -Dbuiltin_xxhash=ON \
  -Darrow=OFF \
  -DGSL_ROOT_DIR="${GSL_ROOT}" \
  -DCMAKE_CXX_STANDARD=17 \
  -Dssl=ON \
  -DOPENSSL_ROOT_DIR="${OPENSSL_ROOT}" \
  -DOPENSSL_INCLUDE_DIR="${OPENSSL_ROOT}/include" \
  -Dpython=ON \
  -Dxrootd=ON \
  -Dbuiltin_xrootd=OFF \
  -DXROOTD_INCLUDE_DIR="${XROOTD_ROOT}/include/xrootd" \
  -DXROOTD_ROOT_DIR="${XROOTD_ROOT}" \
%if %islinux
  -Drfio=OFF \
  -Dcastor=OFF \
  -Ddcache=ON \
  -DDCAP_INCLUDE_DIR="${DCAP_ROOT}/include" \
  -DDCAP_DIR="${DCAP_ROOT}" \
%endif
  -DCMAKE_C_FLAGS="-D__ROOFIT_NOBANNER" \
  -DCMAKE_C_FLAGS="-D__ROOFIT_NOBANNER" \
  -Dgviz=OFF \
  -Dbonjour=OFF \
  -Dodbc=OFF \
  -Dpythia6=OFF \
  -Dpythia8=OFF \
  -Dfitsio=OFF \
  -Dgfal=OFF \
  -Dchirp=OFF \
  -Dsrp=OFF \
  -Ddavix=ON \
  -Dglite=OFF \
  -Dsapdb=OFF \
  -Dalien=OFF \
  -Dmonalisa=OFF \
%if %isdarwin
  -Dbuiltin_afterimage=OFF \
  -Dcocoa=OFF \
  -Dx11=ON \
  -Dcastor=OFF \
  -Drfio=OFF \
  -Ddcache=OFF \
%endif
  -DJPEG_INCLUDE_DIR="${LIBJPEG_TURBO_ROOT}/include" \
  -DJPEG_LIBRARY="${LIBJPEG_TURBO_ROOT}/lib64/libjpeg.%{soext}" \
  -DPNG_INCLUDE_DIRS="${LIBPNG_ROOT}/include" \
  -DPNG_LIBRARY="${LIBPNG_ROOT}/lib/libpng.%{soext}" \
  -Dastiff=ON \
  -DTIFF_INCLUDE_DIR="${LIBTIFF_ROOT}/include" \
  -DTIFF_LIBRARY="${LIBTIFF_ROOT}/lib/libtiff.%{soext}" \
  -DLIBLZMA_INCLUDE_DIR="${XZ_ROOT}/include" \
  -DLIBLZMA_LIBRARY="${XZ_ROOT}/lib/liblzma.%{soext}" \
  -DLIBLZ4_INCLUDE_DIR="${LZ4_ROOT}/include" \
  -DLIBLZ4_LIBRARY="${LZ4_ROOT}/lib/liblz4.%{soext}" \
  -DZLIB_ROOT="${ZLIB_ROOT}" \
  -DZLIB_INCLUDE_DIR="${ZLIB_ROOT}/include" \
  -DCMAKE_PREFIX_PATH="${GSL_ROOT}:${XZ_ROOT};${OPENSSL_ROOT};${GIFLIB_ROOT};${FREETYPE_ROOT};${PYTHON_ROOT};${LIBPNG_ROOT};${PCRE_ROOT};${TBB_ROOT};${OPENBLAS_ROOT};${DAVIX_ROOT};${LZ4_ROOT};${LIBXML2_ROOT}"

# For CMake cache variables: http://www.cmake.org/cmake/help/v3.2/manual/cmake-language.7.html#lists
# For environment variables it's OS specific: http://www.cmake.org/Wiki/CMake_Useful_Variables

#  Required for generated dictionaries during ROOT6 compile/install
ROOT_INCLUDE_PATH=
for DEP in %requiredtools; do
  ROOT_INCLUDE_PATH=$(eval echo $(printf "\${%%s_ROOT}/include" $(echo $DEP | tr "[a-z]-" "[A-Z]_"))):$ROOT_INCLUDE_PATH
done

export ROOT_INCLUDE_PATH
export ROOTSYS="%{i}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN)

%install
cd ../build

# Required for generated dictionaries during ROOT6 compile/install
ROOT_INCLUDE_PATH=
for DEP in %requiredtools; do
  ROOT_INCLUDE_PATH=$(eval echo $(printf "\${%%s_ROOT}/include" $(echo $DEP | tr "[a-z]-" "[A-Z]_"))):$ROOT_INCLUDE_PATH
done

export ROOT_INCLUDE_PATH
export ROOTSYS="%{i}"

ninja -v %{makeprocesses} -l $(getconf _NPROCESSORS_ONLN) install

find %{i} -type f -name '*.py' | xargs chmod -x
grep -R -l '#!.*python' %{i} | xargs chmod +x
perl -p -i -e "s|#!/bin/perl|#!/usr/bin/env perl|" %{i}/bin/memprobe

#Make sure root build directory is not available after the root install is done
#This will catch errors if root remembers the build paths.
cd ..
rm -rf build

%post
%{relocateConfig}etc/cling/llvm/Config/llvm-config.h
