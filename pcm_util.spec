### RPM external pcm_util 1.0

Source: none
BuildRequires: root clhep tinyxml2

%prep


%build

rm -f empty.h
rm -f dummy.modulemap

touch empty.h
echo "module Dummy{}" > dummy.modulemap

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -moduleMapFile=${CLHEP_ROOT}/include/module.modulemap -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m clhep -mByproduct clhep  -I ${CLHEP_ROOT}/include/ empty.h

rm -f dummy_dict.cc
rm -f libDummy.so
rootcling dummy_dict.cc -s ./libDummy.so -moduleMapFile=dummy.modulemap -cxxmodule -m tinyxml2 -mByproduct tinyxml2  -I ${TINYXML2_ROOT}/include/ empty.h


%install

mkdir %{i}/lib
cp clhep.pcm %{i}/lib/.
cp tinyxml2.pcm %{i}/lib/.
