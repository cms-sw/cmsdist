### RPM external pcm_util 1.0

Source: none
BuildRequires: root clhep tinyxml2 boost fftw3

%prep


%build

rm -f *.pcm
rm -f empty.h
rm -f dummy.modulemap

touch empty.h
echo "module Dummy{}" > dummy.modulemap

CLHEP_MM_NAME="module.modulemap"
TINYXML2_MM_NAME="tinyxml2.modulemap"
BOOST_FLAGS="-DBOOST_SPIRIT_THREADSAFE -DPHOENIX_THREADSAFE -DBOOST_MATH_DISABLE_STD_FPCLASSIFY -DBOOST_UUID_RANDOM_PROVIDER_FORCE_POSIX -DBOOST_CONTAINER_FORCEINLINE=inline -DBOOST_UBLAS_INLINE=inline -DBOOST_DATE_TIME_INCLUDE_LIMITED_HEADERS -DBOOST_SP_USE_STD_ALLOCATOR -DBOOST_INTRUSIVE_FORCEINLINE=inline" 


#packages with module maps
for mod in clhep tinyxml2
do
    rootvar="$(echo "${mod}_ROOT" | tr [a-z] [A-Z])"
    mm_name="$(echo "${mod}_MM_NAME" | tr [a-z] [A-Z])"
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -moduleMapFile=${!rootvar}/include/${!mm_name} -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m $mod -mByproduct $mod  -I ${!rootvar}/include/ empty.h
    mkdir -p $mod
    rm -f Dummy.pcm
    mv *.pcm $mod
done

#boost is special
for mod in boost_type_traits boost_algorithm_and_range boost_any boost_mpl boost_intrusive boost_functional boost_archive_and_serialization #boost_date_time
do
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 $BOOST_FLAGS -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m ${mod} -mByproduct ${mod}  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost -I ${FFTW3_ROOT}/include empty.h
done

mkdir -p boost
rm -f Dummy.pcm
mv *.pcm boost/.



%install

mkdir %{i}/lib
rm -f Dummy.pcm
cp -r clhep tinyxml2 boost %{i}/lib/.


