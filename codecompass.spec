### RPM external codecompass 1.0
%define github_user Ericsson
%define tag a45aaeb300e7739980a8c1814eff65cc477052f6
Source: git+https://github.com/%{github_user}/CodeCompass.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: cmake gmake
Requires: thrift odb python sqlite graphviz git java-env boost llvm graphviz libgit2

%prep
%setup -n codecompass-1.0
perl -p -i -e 's|include\(UseJava\)|include\(UseJava\)\ninclude_directories(\${LIBGIT2_INCLUDE_DIR} \${Graphviz_INCLUDE_DIR} \${BOOST_INCLUDE_DIRS})|' ./CMakeLists.txt
perl -p -i -e 's|include\(UseJava\)|include\(UseJava\)\nset\(CMAKE_JAVA_COMPILE_FLAGS -nowarn -encoding UTF8\)|' ./CMakeLists.txt
perl -p -i -e 's|enable_testing\(\)||' ./CMakeLists.txt
perl -p -i -e 's|#include <memory>|#include <memory>\n#include <vector>|' ./model/include/model/buildaction.h
perl -p -i -e 's|--std c\+\+11|--std c\+\+14|' ./Config.cmake 
echo 'list(APPEND ODBFLAGS -I${BOOST_INCLUDE_DIRS})' >> ./Config.cmake
perl -p -i -e 's|#include <string>|#include <string>\n#include <set>|' ./plugins/cpp/model/include/model/cppentity.h
perl -p -i -e 's|#include <boost/shared_ptr.hpp>||' webserver/include/webserver/thrifthandler.h
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' webserver/include/webserver/thrifthandler.h

perl -p -i -e 's|#include <boost/shared_ptr.hpp>|#include <memory>|' ./plugins/search/indexer/src/indexerprocess.cpp
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' ./plugins/search/indexer/src/indexerprocess.cpp
perl -p -i -e 's|#include <boost/shared_ptr.hpp>|#include <memory>|' ./plugins/search/service/include/service/serviceprocess.h
perl -p -i -e 's|boost::shared_ptr|std::shared_ptr|g' ./plugins/search/service/include/service/serviceprocess.h
perl -p -i -e 's|add_subdirectory\(test\)||' ./plugins/cpp/CMakeLists.txt
perl -p -i -e 's|git2|-L\${LIBGIT2_INCLUDE_DIR}/../lib  git2|' ./plugins/git/parser/CMakeLists.txt
perl -p -i -e 's|git2|-L\${LIBGIT2_INCLUDE_DIR}/../lib  git2|' ./plugins/git/service/CMakeLists.txt
perl -p -i -e 's|gvc|-L\${Graphviz_INCLUDE_DIR}/../lib  gvc|' ./plugins/cpp/service/CMakeLists.txt
rm lib/java/libthrift-0.10.0.jar
curl -O https://repo1.maven.org/maven2/org/apache/thrift/libthrift/0.11.0/libthrift-0.11.0.jar
cp libthrift-0.11.0.jar lib/java

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
cd cmake-build
make install
rm -rf %{i}/share/codecompass/webgui/
