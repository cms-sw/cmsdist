### RPM external pcm_util 1.0

Source: none
Requires: root clhep tinyxml2 boost fftw3 cuda python3 hepmc tbb gcc

%prep


%build

rm -f *.pcm
rm -f empty.h
rm -f dummy.modulemap

touch empty.h
echo "module Dummy{}" > dummy.modulemap

CLHEP_MM_NAME="module.modulemap"
TINYXML2_MM_NAME="tinyxml2.modulemap"
CUDA_MM_NAME="cuda.modulemap"
HEPMC_MM_NAME="hepmc.modulemap"
TBB_MM_NAME="module.modulemap"

GCC_GLIBCXX_VERSION=$(gcc -dumpversion | tr '.' '0')
BOOST_FLAGS="-DBOOST_SPIRIT_THREADSAFE -DPHOENIX_THREADSAFE -DBOOST_MATH_DISABLE_STD_FPCLASSIFY -DBOOST_UUID_RANDOM_PROVIDER_FORCE_POSIX" 
TBB_FLAGS="-DTBB_USE_GLIBCXX_VERSION=${GCC_GLIBCXX_VERSION} -DTBB_SUPPRESS_DEPRECATED_MESSAGES -DTBB_PREVIEW_RESUMABLE_TASKS=1"
CLHEP_FLAGS=""
TINYXML2_FLAGS=""
HEPMC_FLAGS=""


#packages with module maps
for mod in clhep tinyxml2 cuda HepMC tbb
do
    rootvar="$(echo "${mod}_ROOT" | tr [a-z] [A-Z])"
    mm_name="$(echo "${mod}_MM_NAME" | tr [a-z] [A-Z])"
    mm_flags="$(echo "${mod}_FLAGS" | tr [a-z] [A-Z])"
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 ${!mm_flags} -moduleMapFile=${!rootvar}/include/${!mm_name} -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m $mod -mByproduct $mod  -I ${!rootvar}/include/ empty.h
    mkdir -p $mod
    rm -f Dummy.pcm
    mv *.pcm $mod
done

#boost is special

#rm -f dummy_dict*.cc
#rm -f libDummy*.so
#
#echo "boost_type_traits boost_algorithm_and_range boost_any boost_mpl boost_intrusive boost_functional boost_archive_and_serialization boost_date_time boost_iterator_adaptors boost_endian" | xargs -I myMod -d ' ' -n 1 -P 4 rootcling dummy_dict_myMod.cc -v2 $BOOST_FLAGS -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy_myMod.so -moduleMapFile=dummy.modulemap -cxxmodule -m myMod -mByproduct myMod  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost -I ${FFTW3_ROOT}/include empty.h
#rm -f dummy_dict*.cc
#rm -f libDummy*.so

for mod in boost_rational boost_type_traits boost_algorithm_and_range boost_any boost_mpl boost_intrusive boost_functional boost_archive_and_serialization boost_date_time boost_iterator_adaptors boost_endian boost_python boost_program_options boost_thread boost_iostreams boost_spirit boost_multi_index_container
do
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 $BOOST_FLAGS -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m ${mod} -mByproduct ${mod}  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost -I ${FFTW3_ROOT}/include -I ${PYTHON_ROOT}/include/python2.7 empty.h
done

mkdir -p boost
rm -f Dummy*.pcm
rm -f libDummy*.pcm
mv *.pcm boost/.



%install

mkdir %{i}/lib
rm -f Dummy*.pcm
rm -f libDummy*.pcm
cp -r clhep tinyxml2 boost cuda HepMC tbb  %{i}/lib/.

