### RPM lcg root 6.39.1
## INITENV +PATH PYTHON3PATH %{i}/lib
## INITENV SET ROOTSYS %{i}
## INCLUDE compilation_flags
## INCLUDE cpp-standard
%define tag 34ad2bac477aef8d6e4ee65b18d6dc2c90579eb8
%define branch cms/master/ed64fd3dce4

%define github_user cms-sw
Source: git+https://github.com/%{github_user}/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

Patch0: root_lazy
Patch2: root_cuda
Patch3: root_modules_211215
#Patch4: root_avoid_load
 
BuildRequires: cmake cms-ninja

Requires: curl gsl libjpeg-turbo libpng libtiff giflib pcre2 python3 fftw3 xz xrootd libxml2 zlib davix tbb OpenBLAS py3-numpy lz4 freetype zstd json
%{!?without_cuda:Requires: cuda}

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
%get_config_sub graf2d/asimage/src/libAfterImage/config.sub
%get_config_guess graf2d/asimage/src/libAfterImage/config.guess
chmod +x graf2d/asimage/src/libAfterImage/config.{sub,guess}

%patch0 -p1
%patch2 -p1
%patch3 -p1
#patch4 -p1

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
%if %{is_debug_build root/llvm}
  -DLLVM_BUILD_TYPE=Debug \
%else
  -DLLVM_BUILD_TYPE=Release \
%endif
  -DCMAKE_INSTALL_PREFIX="%{i}" \
  -DCMAKE_C_COMPILER=gcc \
  -DCMAKE_CXX_COMPILER=g++ \
  -DCMAKE_Fortran_COMPILER=gfortran \
  -DCMAKE_LINKER=ld \
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -Druntime_cxxmodules=ON \
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
  -Dtmva-pymva=ON \
  -DFFTW_INCLUDE_DIR="${FFTW3_ROOT}/include" \
  -DFFTW_LIBRARY="${FFTW3_ROOT}/lib/libfftw3.%{soext}" \
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
  -Dbuiltin_xxhash=ON \
  -Dbuiltin_nlohmannjson=OFF \
  -Darrow=OFF \
  -DGSL_ROOT_DIR="${GSL_ROOT}" \
  -DGSL_CBLAS_LIBRARY="${OPENBLAS_ROOT}/lib/libopenblas.%{soext}" \
  -DGSL_CBLAS_LIBRARY_DEBUG="${OPENBLAS_ROOT}/lib/libopenblas.%{soext}" \
  -DCMAKE_CXX_STANDARD=%{cms_cxx_standard} \
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
  -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

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
ninja -v %{makeprocesses} clang

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
mkdir -p %{i}/etc/cling/bin
cp -P interpreter/llvm-project/llvm/bin/clang %{i}/etc/cling/bin/
cp -P interpreter/llvm-project/llvm/bin/clang-* %{i}/etc/cling/bin/

# Generate cuda.pcm if CUDA is available
%if 0%{!?without_cuda:1}
echo '#include <cuda_runtime.h>' | %{i}/bin/root -b -n -l
%endif

find %{i} -type f -name '*.py' | xargs chmod -x
grep -rlI '#!.*python' %{i} | xargs chmod +x
for p in $(grep -rlI -m1 '^#\!.*python' %i/bin %i/etc) ; do
  lnum=$(grep -n -m1 '^#\!.*python' $p | sed 's|:.*||')
  sed -i -e "${lnum}c#!/usr/bin/env python3" $p
done

%post
%{relocateConfig}bin/root-config
%{relocateConfig}cmake/ROOTConfig-targets.cmake
%{relocateConfig}etc/notebook/jupyter_notebook_config.py
%{relocateConfig}include/RConfigOptions.h
%{relocateConfig}include/compiledata.h
