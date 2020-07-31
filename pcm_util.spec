### RPM external pcm_util 1.0

Source: none
BuildRequires: root clhep tinyxml2 boost

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
for mod in boost_type_traits boost_algorithm_and_range boost_any boost_mpl boost_intrusive boost_functional boost_archive_and_serialization
do
    rm -f dummy_dict.cc
    rm -f libDummy.so
    rootcling dummy_dict.cc -v2 $BOOST_FLAGS -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m ${mod} -mByproduct ${mod}  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h
done

mkdir -p boost
rm -f Dummy.pcm
mv *.pcm boost/.

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -moduleMapFile=${CLHEP_ROOT}/include/module.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m clhep -mByproduct clhep  -I ${CLHEP_ROOT}/include/ empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v4 -moduleMapFile=${TINYXML2_ROOT}/include/tinyxml2.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m tinyxml2 -mByproduct tinyxml2  -I ${TINYXML2_ROOT}/include/ empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v4 -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_type_traits -mByproduct boost_type_traits  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_CONTAINER_FORCEINLINE=inline -DBOOST_UBLAS_INLINE=inline -DBOOST_DATE_TIME_INCLUDE_LIMITED_HEADERS -DBOOST_SP_USE_STD_ALLOCATOR -DBOOST_INTRUSIVE_FORCEINLINE=inline -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_algorithm_and_range -mByproduct boost_algorithm_and_range  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_CONTAINER_FORCEINLINE=inline -DBOOST_UBLAS_INLINE=inline -DBOOST_DATE_TIME_INCLUDE_LIMITED_HEADERS -DBOOST_SP_USE_STD_ALLOCATOR -DBOOST_INTRUSIVE_FORCEINLINE=inline -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_any -mByproduct boost_any  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h


#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_mpl -mByproduct boost_mpl -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -DBOOST_INTRUSIVE_FORCEINLINE=inline -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_intrusive -mByproduct boost_intrusive -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_functional -mByproduct boost_functional -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h


%install

mkdir %{i}/lib
rm -f Dummy.pcm
cp -r clhep tinyxml2 boost %{i}/lib/.


