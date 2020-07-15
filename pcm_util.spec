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

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -moduleMapFile=${CLHEP_ROOT}/include/module.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m clhep -mByproduct clhep  -I ${CLHEP_ROOT}/include/ empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -v4 -moduleMapFile=${TINYXML2_ROOT}/include/tinyxml2.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m tinyxml2 -mByproduct tinyxml2  -I ${TINYXML2_ROOT}/include/ empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -v4 -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_type_traits -mByproduct boost_type_traits  -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

#rm -f dummy_dict.cc
#rm -f libDummy.so
#rootcling dummy_dict.cc -v2 -DBOOST_CONTAINER_FORCEINLINE=inline -DBOOST_INTRUSIVE_DISABLE_FORCEINLINE -DBOOST_SP_USE_STD_ALLOCATOR -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_modules_wrapper -mByproduct boost_modules_wrapper -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_mpl -mByproduct boost_mpl -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -DBOOST_INTRUSIVE_FORCEINLINE=inline -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_intrusive -mByproduct boost_intrusive -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -v2 -DBOOST_SP_USE_STD_ALLOCATOR -moduleMapFile=${BOOST_ROOT}/include/boost/boost.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m boost_functional -mByproduct boost_functional -I ${BOOST_ROOT}/include/ -I ${BOOST_ROOT}/include/boost empty.h


%install

mkdir %{i}/lib
rm Dummy.pcm
cp *.pcm %{i}/lib/.

