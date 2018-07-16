### RPM external codecompass 1.0
%define github_user Ericsson
%define tag a45aaeb300e7739980a8c1814eff65cc477052f6
Source: git+https://github.com/%{github_user}/CodeCompass.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
BuildRequires: cmake
Requires: thrift odb python sqlite graphviz git java-env boost llvm graphviz libgit2

%prep
%setup -n codecompass-1.0
perl -p -i -e 's|include\(UseJava\)|include\(UseJava\)\ninclude_directories(\${LIBGIT2_INCLUDE_DIR} \${Graphviz_INCLUDE_DIR} \${BOOST_INCLUDE_DIRS})|' ./CMakeLists.txt
perl -p -i -e 's|enable_testing\(\)||' ./CMakeLists.txt
perl -p -i -e 's|#include <memory>|#include <memory>\n#include <vector>|' ./model/include/model/buildaction.h
perl -p -i -e 's|--std c\+\+11|--std c\+\+14|' ./Config.cmake 
perl -p -e -e 's|--default-pointer "std::shared_ptr"\)|--default-pointer "std::shared_ptr"\)\nlist(APPEND ODBATGS -I\${BOOST_INCLUDE_DIRS}|' ./Config.cmake
perl -p -i -e 's|#include <string>|#include <string>\n#include <set>|' ./plugins/cpp/model/include/model/cppentity.h
perl -p -i -e 's|#include <boost/shared_ptr.hpp>||' webserver/include/webserver/thrifthandler.h
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' webserver/include/webserver/thrifthandler.h

perl -p -i -e 's|#include <boost/shared_ptr.hpp>|#include <memory>|' ./plugins/search/indexer/src/indexerprocess.cpp
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' ./plugins/search/indexer/src/indexerprocess.cpp
perl -p -i -e 's|#include <boost/shared_ptr.hpp>|#include <memory>|' ./plugins/search/service/include/service/serviceprocess.h
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' ./plugins/search/service/include/service/serviceprocess.h
perl -p -i -e 's|add_subdirectory\(test\)||' ./plugins/cpp/CMakeLists.txt

%build
export CMAKE_PREFIX_PATH=${BOOST_ROOT}:${THRIFT_ROOT}:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${LLVM_ROOT}/share/llvm/cmake:$CMAKE_PREFIX_PATH
export CMAKE_PREFIX_PATH=${ODB_ROOT}:$CMAKE_PREFIX_PATH
export PATH=${THRIFT_ROOT}/bin:$PATH
export PATH=${ODB_ROOT}/bin:$PATH
mkdir -p cmake-build
cd cmake-build
cmake -DCMAKE_INSTALL_PREFIX=%{i} -DDATABASE=sqlite -DCMAKE_BUILD_TYPE=RelWithDebug -DPC_LIBTHRIFT_INCLUDE_DIR=${THRIFT_ROOT}/include -DBOOST_ROOT=${BOOST_ROOT} -DBOOST_INCLUDE_DIRS=${BOOST_ROOT}/include -DGraphviz_INCLUDE_DIR=${GRAPHVIZ_ROOT}/include -DLIBGIT2_INCLUDE_DIR=${LIBGIT2_ROOT}/include .. 
make VERBOSE=1 -k -j %{compiling_processes}

%install
make install
