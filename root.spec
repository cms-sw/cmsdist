### RPM lcg root 6.26.11
## INITENV +PATH PYTHON3PATH %{i}/lib
## INITENV SET ROOTSYS %{i}
## INCLUDE compilation_flags
%define tag fe824a0d8806a5484c3cc1530d60107774c59257
%define branch cms/v6-26-00-patches/a25c523160

%define github_user cms-sw
Source: git+https://github.com/%{github_user}/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake ninja

Requires: gsl libjpeg-turbo libpng libtiff giflib pcre python3 fftw3 xz xrootd libxml2 zlib davix tbb OpenBLAS py3-numpy lz4 freetype zstd

%ifos linux
Requires: dcap
%endif

%define soext so
%ifarch darwin
%define soext dylib
%endif

%define keep_archives true

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build
mkdir ../build
cd ../build

export CFLAGS=-D__ROOFIT_NOBANNER
export CXXFLAGS=-D__ROOFIT_NOBANNER
%if "%{?arch_build_flags}"
export CFLAGS="${CFLAGS} %{arch_build_flags}"
export CXXFLAGS="${CXXFLAGS} %{arch_build_flags}"
%endif

cmake ../%{n}-%{realversion} \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=%{cmake_build_type} \
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
  -Dtmva=ON \
  -DPython3_EXECUTABLE="${PYTHON3_ROOT}/bin/python3" \
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
  -Dbuiltin_tbb=OFF \
  -Dbuiltin_pcre=OFF \
  -Dbuiltin_freetype=OFF \
  -Dbuiltin_zlib=OFF \
  -Dbuiltin_lzma=OFF \
  -Dbuiltin_gsl=OFF \
  -Dbuiltin_glew=ON \
  -Dbuiltin_ftgl=ON \
  -Dbuiltin_gl2ps=ON \
  -Dbuiltin_afterimage=ON \
  -Dbuiltin_xxhash=ON \
  -Dbuiltin_nlohmannjson=ON \
  -Darrow=OFF \
  -DGSL_ROOT_DIR="${GSL_ROOT}" \
  -DGSL_CBLAS_LIBRARY="${OPENBLAS_ROOT}/lib/libopenblas.%{soext}" \
  -DGSL_CBLAS_LIBRARY_DEBUG="${OPENBLAS_ROOT}/lib/libopenblas.%{soext}" \
  -DCMAKE_CXX_STANDARD=17 \
  -Dssl=ON \
  -Dpyroot=ON \
  -Dxrootd=ON \
  -Dbuiltin_xrootd=OFF \
  -DXROOTD_INCLUDE_DIR="${XROOTD_ROOT}/include/xrootd" \
  -DXROOTD_ROOT_DIR="${XROOTD_ROOT}" \
%ifos linux
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
%ifarch darwin
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
  -DLZ4_INCLUDE_DIR="${LZ4_ROOT}/include" \
  -DLZ4_LIBRARY="${LZ4_ROOT}/lib/liblz4.%{soext}" \
  -DZLIB_ROOT="${ZLIB_ROOT}" \
  -DZLIB_INCLUDE_DIR="${ZLIB_ROOT}/include" \
  -DZSTD_ROOT="${ZSTD_ROOT}" \
  -DCMAKE_PREFIX_PATH="${LZ4_ROOT};${GSL_ROOT};${XZ_ROOT};${GIFLIB_ROOT};${FREETYPE_ROOT};${PYTHON3_ROOT};${LIBPNG_ROOT};${PCRE_ROOT};${TBB_ROOT};${OPENBLAS_ROOT};${DAVIX_ROOT};${LIBXML2_ROOT};${ZSTD_ROOT}"

# For CMake cache variables: http://www.cmake.org/cmake/help/v3.2/manual/cmake-language.7.html#lists
# For environment variables it's OS specific: http://www.cmake.org/Wiki/CMake_Useful_Variables

#  Required for generated dictionaries during ROOT6 compile/install
ROOT_INCLUDE_PATH=
for DEP in %requiredtools; do
  ROOT_INCLUDE_PATH=$(eval echo $(printf "\${%%s_ROOT}/include" $(echo $DEP | tr "[a-z]-" "[A-Z]_"))):$ROOT_INCLUDE_PATH
done

export ROOT_INCLUDE_PATH
export ROOTSYS="%{i}"

ninja -v %{makeprocesses}

%install
cd ../build

# Required for generated dictionaries during ROOT6 compile/install
ROOT_INCLUDE_PATH=
for DEP in %requiredtools; do
  ROOT_INCLUDE_PATH=$(eval echo $(printf "\${%%s_ROOT}/include" $(echo $DEP | tr "[a-z]-" "[A-Z]_"))):$ROOT_INCLUDE_PATH
done

export ROOT_INCLUDE_PATH
export ROOTSYS="%{i}"

ninja -v %{makeprocesses} install

find %{i} -type f -name '*.py' | xargs chmod -x
grep -rlI '#!.*python' %{i} | xargs chmod +x
for p in $(grep -rlI -m1 '^#\!.*python' %i/bin) ; do
  lnum=$(grep -n -m1 '^#\!.*python' $p | sed 's|:.*||')
  sed -i -e "${lnum}c#!/usr/bin/env python3" $p
done

#Make sure root build directory is not available after the root install is done
#This will catch errors if root remembers the build paths.
cd ..
rm -rf build

%post
%{relocateConfig}bin/root-config
%{relocateConfig}cmake/ROOTConfig-targets.cmake
%{relocateConfig}config/Makefile.config
%{relocateConfig}etc/notebook/jupyter_notebook_config.py
%{relocateConfig}include/RConfigOptions.h
%{relocateConfig}include/compiledata.h
