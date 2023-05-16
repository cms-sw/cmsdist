### RPM external pcm_util 2.0

Source: none 
Requires: root clhep tinyxml2 boost fftw3 cuda python3 hepmc tbb gcc py3-pybind11 fmt xerces-c dd4hep hls

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
BOOST_MM_NAME="module.modulemap"
HLS_MM_NAME="hls.modulemap"

BOOST_MODDIR="include/boost"
 
PYBIND11_MODPACK="py3_pybind11"
XERCESC_MODPACK="xerces_c"

GCC_GLIBCXX_VERSION=$(gcc -dumpversion | tr '.' '0')
BOOST_FLAGS="-DBOOST_SPIRIT_THREADSAFE -DPHOENIX_THREADSAFE -DBOOST_MATH_DISABLE_STD_FPCLASSIFY -DBOOST_UUID_RANDOM_PROVIDER_FORCE_POSIX -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost -I ${FFTW3_ROOT}/include -I ${PYTHON3_ROOT}/include/python%{cms_python3_major_minor_version}"

TBB_FLAGS="-DTBB_USE_GLIBCXX_VERSION=${GCC_GLIBCXX_VERSION} -DTBB_SUPPRESS_DEPRECATED_MESSAGES -DTBB_PREVIEW_RESUMABLE_TASKS=1 -DTBB_PREVIEW_TASK_GROUP_EXTENSIONS=1"
PYBIND11_FLAGS="-I$PYTHON3_ROOT/include/python%{cms_python3_major_minor_version}/"

function check_var() {
   var=$1
   default=$2
   if [ -z ${!var+x} ]; 
   then
      declare -g "${var}"=${default}
   fi
}

packlist="tbb pybind11 clhep tinyxml2 cuda HepMC fmt xercesc dd4hep boost hls"
for mod in $packlist
do
    modpack="$(echo "${mod}_MODPACK" | tr [a-z] [A-Z])"
    check_var $modpack $mod
    rootvar="$(echo "${!modpack}_ROOT" | tr [a-z] [A-Z])"
    check_var $rootvar "include/"
    mm_name="$(echo "${mod}_MM_NAME" | tr [a-z] [A-Z])"
    check_var $mm_name "module.modulemap"
    mm_flags="$(echo "${mod}_FLAGS" | tr [a-z] [A-Z])"
    check_var $mm_flags ""
    mm_incdir="$(echo "${mod}_INCDIR" | tr [a-z] [A-Z])"
    check_var $mm_incdir "include"
    mm_moddir="$(echo "${mod}_MODDIR" | tr [a-z] [A-Z])"
    check_var $mm_moddir "include"

    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 ${!mm_flags} -moduleMapFile=${!rootvar}/${!mm_moddir}/${!mm_name} -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m $mod -mByproduct $mod  -I${!rootvar}/${!mm_incdir} empty.h
    mkdir -p $mod
    rm -f Dummy.pcm
    mv *.pcm $mod
done

%install

mkdir %{i}/lib
rm -f Dummy*.pcm
rm -f libDummy*.pcm
packlist="tbb pybind11 clhep tinyxml2 cuda HepMC fmt xercesc dd4hep boost hls"
cp -r $packlist %{i}/lib/.

