### RPM external pcm_util 1.0

Source: none 
Requires: root clhep tinyxml2 boost fftw3 cuda python3 hepmc tbb gcc py3-pybind11                  

%prep


%build

rm -f *.pcm
rm -f empty.h
rm -f dummy.modulemap

touch empty.h
echo "module Dummy{}" > dummy.modulemap

CLHEP_MM_NAME="clhep.modulemap"
TINYXML2_MM_NAME="tinyxml2.modulemap"
CUDA_MM_NAME="cuda.modulemap"
HEPMC_MM_NAME="hepmc.modulemap"
TBB_MM_NAME="module.modulemap"
PYBIND11_MM_NAME="module.modulemap"

CLHEP_INCDIR="include/"
TINYXML2_INCDIR="include/"
CUDA_INCDIR="include/"
HEPMC_INCDIR="include/"
TBB_INCDIR="include/"
PYBIND11_INCDIR="${PYTHON3_LIB_SITE_PACKAGES}/pybind11/include"

CLHEP_MODDIR="include"
TINYXML2_MODDIR="include"
CUDA_MODDIR="include"
HEPMC_MODDIR="include"
TBB_MODDIR="include"
PYBIND11_MODDIR="${PYTHON3_LIB_SITE_PACKAGES}/pybind11/include"
 
CLHEP_MODPACK="clhep"
TINYXML2_MODPACK="tinyxml2"
CUDA_MODPACK="cuda"
HEPMC_MODPACK="hepmc"
TBB_MODPACK="tbb"
PYBIND11_MODPACK="py3_pybind11"

GCC_GLIBCXX_VERSION=$(gcc -dumpversion | tr '.' '0')
BOOST_FLAGS="-DBOOST_SPIRIT_THREADSAFE -DPHOENIX_THREADSAFE -DBOOST_MATH_DISABLE_STD_FPCLASSIFY -DBOOST_UUID_RANDOM_PROVIDER_FORCE_POSIX" 
TBB_FLAGS="-DTBB_USE_GLIBCXX_VERSION=${GCC_GLIBCXX_VERSION} -DTBB_SUPPRESS_DEPRECATED_MESSAGES -DTBB_PREVIEW_RESUMABLE_TASKS=1"
CLHEP_FLAGS=""
TINYXML2_FLAGS=""
HEPMC_FLAGS=""
PYBIND11_FLAGS="-I$PYTHON3_ROOT/include/python%{cms_python3_major_minor_version}/"

#packages with module maps
for mod in tbb pybind11 clhep tinyxml2 cuda HepMC
do
    modpack="$(echo "${mod}_MODPACK" | tr [a-z] [A-Z])"
    rootvar="$(echo "${!modpack}_ROOT" | tr [a-z] [A-Z])"
    mm_name="$(echo "${mod}_MM_NAME" | tr [a-z] [A-Z])"
    mm_flags="$(echo "${mod}_FLAGS" | tr [a-z] [A-Z])"
    mm_incdir="$(echo "${mod}_INCDIR" | tr [a-z] [A-Z])"
    mm_moddir="$(echo "${mod}_MODDIR" | tr [a-z] [A-Z])"
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 ${!mm_flags} -moduleMapFile=${!rootvar}/${!mm_moddir}/${!mm_name} -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m $mod -mByproduct $mod  -I${!rootvar}/${!mm_incdir} empty.h
    mkdir -p $mod
    rm -f Dummy.pcm
    mv *.pcm $mod
done

for mod in boost
#for mod in rational type_traits algorithm range intrusive_ptr functional archive_and_serialization date_time iterator_adaptors endian program_options thread iostreams multi_index_container spirit python 
do
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 $BOOST_FLAGS -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m ${mod} -mByproduct ${mod}  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost -I ${FFTW3_ROOT}/include -I ${PYTHON3_ROOT}/include/python%{cms_python3_major_minor_version} empty.h
done

mkdir -p boost
rm -f Dummy*.pcm
rm -f libDummy*.pcm
mv *.pcm boost/.

%install

mkdir %{i}/lib
rm -f Dummy*.pcm
rm -f libDummy*.pcm
cp -r clhep tinyxml2 boost cuda HepMC tbb pybind11  %{i}/lib/.

