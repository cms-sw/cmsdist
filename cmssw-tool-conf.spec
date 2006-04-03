
### RPM cms cmssw-tool-conf 132
Source0: none

Requires: gcc

Requires: gcc

Requires: lcgaa
Requires: coral
Requires: pool
Requires: seal
Requires: ignominy
Requires: xdaq
Requires: geant4
Requires: hepmc
Requires: heppdt
Requires: clhep
Requires: rfio
Requires: zlib
Requires: python
Requires: boost
Requires: xerces-c
Requires: root
Requires: root

Requires: root

Requires: root

Requires: uuid
Requires: gsl
Requires: sqlite
Requires: oracle
Requires: unixodbc
Requires: myodbc
Requires: mysqlpp
Requires: mysql
Requires: gccxml
Requires: python
Requires: boost
Requires: elementtree

Requires: bz2lib
Requires: pcre
Requires: dcap
Requires: rulechecker
Requires: cppunit
Requires: qt
Requires: soqt
Requires: coin

Requires: simage
Requires: openssl
Requires: hippodraw
Requires: qutexmlrpc
Requires: frontier_client
Requires: genser
Requires: genser

Requires: doxygen
Requires: meschach
Requires: iguana
%prep
%build
(echo "ARCHITECTURE:%{cmsplatf}"
 echo "SCRAM_BASEPATH:%{instroot}/external"

%if "%{?use_system_gcc:set}" == "set"
  echo "TOOL:cxxcompiler:"
       echo "  +GCC_BASE:/none"
       echo "  +CC:$(which gcc)"
       echo "  +CXX:$(which c++)"
       echo "  +PATH:/none"  # useless, toolbox says value=""
       echo "  +LD_LIBRARY_PATH:/none" # useless, toolbox says value=""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$(which g77)"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-set"
echo "TOOL:cxxcompiler:"
       echo "  +GCC_BASE:$CCACHE_ROOT"
eval        "echo \"  +CC:$CCACHE_ROOT/bin/gcc\""
eval        "echo \"  +CXX:$CCACHE_ROOT/bin/c++\""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-" 
echo "TOOL:cxxcompiler:"
       echo "  +GCC_BASE:$GCC_ROOT"
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif


echo "TOOL:ccompiler:"
eval "echo \"  +CCOMPILER_BASE:\${CCOMPILER_ROOT}\""
eval "echo \"  +PATH:\${CCOMPILER_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${CCOMPILER_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${CCOMPILER_ROOT}/include\""


echo "TOOL:lcgaa:"
eval "echo \"  +LCGAA_BASE:\${LCGAA_ROOT}\""
eval "echo \"  +PATH:\${LCGAA_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${LCGAA_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${LCGAA_ROOT}/include\""

echo "TOOL:coral:"
echo "  +CORAL_BASE:$CORAL_ROOT"
echo "  +INCLUDE:$CORAL_ROOT/src"

echo "TOOL:pool:"
echo "  +POOL_BASE:$POOL_ROOT"

echo "TOOL:seal:"
echo "  +SEAL_BASE:$SEAL_ROOT"


echo "TOOL:ignominy:"
eval "echo \"  +IGNOMINY_BASE:\${IGNOMINY_ROOT}\""
eval "echo \"  +PATH:\${IGNOMINY_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${IGNOMINY_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${IGNOMINY_ROOT}/include\""


echo "TOOL:xdaq:"
eval "echo \"  +XDAQ_BASE:\${XDAQ_ROOT}\""
eval "echo \"  +PATH:\${XDAQ_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${XDAQ_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${XDAQ_ROOT}/include\""

echo "TOOL:geant4:"
echo "  +GEANT4_BASE:$GEANT4_ROOT"
echo "  +GEANT4_SHARE_BASE:$GEANT4_ROOT"
echo "  +LIBDIR:$GEANT4_ROOT/lib/$(uname)-g++"
echo "  +INCLUDE:$GEANT4_ROOT/include"
echo "  +G4SRC:$GEANT4_ROOT/source"
echo "  +NeutronHPCrossSections:$G4NDL_PATH"
echo "  +G4LEVELGAMMADATA:$PHOTON_EVAPORATION_PATH"
echo "  +G4RADIOACTIVEDATA:$RADIATIVE_DECAY_PATH"
echo "  +G4LEDATA:$G4EMLOW_PATH"


echo "TOOL:hepmc:"
eval "echo \"  +HEPMC_BASE:\${HEPMC_ROOT}\""
eval "echo \"  +PATH:\${HEPMC_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${HEPMC_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${HEPMC_ROOT}/include\""


echo "TOOL:heppdt:"
eval "echo \"  +HEPPDT_BASE:\${HEPPDT_ROOT}\""
eval "echo \"  +PATH:\${HEPPDT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${HEPPDT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${HEPPDT_ROOT}/include\""


echo "TOOL:clhep:"
eval "echo \"  +CLHEP_BASE:\${CLHEP_ROOT}\""
eval "echo \"  +PATH:\${CLHEP_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${CLHEP_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${CLHEP_ROOT}/include\""


echo "TOOL:rfio:"
eval "echo \"  +RFIO_BASE:\${RFIO_ROOT}\""
eval "echo \"  +PATH:\${RFIO_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${RFIO_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${RFIO_ROOT}/include\""


echo "TOOL:zlib:"
eval "echo \"  +ZLIB_BASE:\${ZLIB_ROOT}\""
eval "echo \"  +PATH:\${ZLIB_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ZLIB_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ZLIB_ROOT}/include\""

PYTHON_MAJOR=$(echo $PYTHON_VERSION | sed 's/\.[0-9]*$//')
echo "TOOL:python:"
echo "  +PYTHON_BASE:$PYTHON_ROOT"
echo "  +LIBDIR:$PYTHON_ROOT/lib/python$PYTHON_MAJOR/config"
echo "  +INCLUDE:$PYTHON_ROOT/include/python$PYTHON_MAJOR"
echo "  +PATH:$PYTHON_ROOT/bin"


echo "TOOL:boost:"
eval "echo \"  +BOOST_BASE:\${BOOST_ROOT}\""
eval "echo \"  +PATH:\${BOOST_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${BOOST_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${BOOST_ROOT}/include\""

echo "TOOL:xerces-c:"
eval "echo \"  +XERCESC_BASE:\${XERCES_C_ROOT}\""
eval "echo \"  +XERCES_C_BASE:\${XERCES_C_ROOT}\""
eval "echo \"  +PATH:\${XERCES_C_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${XERCES_C_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${XERCES_C_ROOT}/include\""


echo "TOOL:root:"
eval "echo \"  +ROOT_BASE:\${ROOT_ROOT}\""
eval "echo \"  +PATH:\${ROOT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ROOT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ROOT_ROOT}/include\""


echo "TOOL:rootrflx:"
eval "echo \"  +ROOTRFLX_BASE:\${ROOTRFLX_ROOT}\""
eval "echo \"  +PATH:\${ROOTRFLX_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ROOTRFLX_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ROOTRFLX_ROOT}/include\""


echo "TOOL:rootcore:"
eval "echo \"  +ROOTCORE_BASE:\${ROOTCORE_ROOT}\""
eval "echo \"  +PATH:\${ROOTCORE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ROOTCORE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ROOTCORE_ROOT}/include\""


echo "TOOL:rootinteractive:"
eval "echo \"  +ROOTINTERACTIVE_BASE:\${ROOTINTERACTIVE_ROOT}\""
eval "echo \"  +PATH:\${ROOTINTERACTIVE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ROOTINTERACTIVE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ROOTINTERACTIVE_ROOT}/include\""


echo "TOOL:uuid:"
eval "echo \"  +UUID_BASE:\${UUID_ROOT}\""
eval "echo \"  +PATH:\${UUID_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${UUID_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${UUID_ROOT}/include\""


echo "TOOL:gsl:"
eval "echo \"  +GSL_BASE:\${GSL_ROOT}\""
eval "echo \"  +PATH:\${GSL_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${GSL_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${GSL_ROOT}/include\""


echo "TOOL:sqlite:"
eval "echo \"  +SQLITE_BASE:\${SQLITE_ROOT}\""
eval "echo \"  +PATH:\${SQLITE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${SQLITE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${SQLITE_ROOT}/include\""

echo "TOOL:oracle:"
echo "  +ORACLE_BASE:$ORACLE_ROOT"
echo "  +PATH:$ORACLE_ROOT/bin"
echo "  +LIBDIR:$ORACLE_ROOT/lib"
echo "  +INCLUDE:$ORACLE_ROOT/include"
echo "  +TNS_ADMIN:$ORACLE_ROOT/admin"


echo "TOOL:unixodbc:"
eval "echo \"  +UNIXODBC_BASE:\${UNIXODBC_ROOT}\""
eval "echo \"  +PATH:\${UNIXODBC_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${UNIXODBC_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${UNIXODBC_ROOT}/include\""


echo "TOOL:myodbc:"
eval "echo \"  +MYODBC_BASE:\${MYODBC_ROOT}\""
eval "echo \"  +PATH:\${MYODBC_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${MYODBC_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${MYODBC_ROOT}/include\""


echo "TOOL:mysqlpp:"
eval "echo \"  +MYSQLPP_BASE:\${MYSQLPP_ROOT}\""
eval "echo \"  +PATH:\${MYSQLPP_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${MYSQLPP_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${MYSQLPP_ROOT}/include\""

echo "TOOL:mysql:"
eval "echo \"  +MYSQL_BASE:\${MYSQL_ROOT}\""
eval "echo \"  +PATH:\${MYSQL_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${MYSQL_ROOT}/lib/mysql\""
eval "echo \"  +INCLUDE:\${MYSQL_ROOT}/include/mysql\""


echo "TOOL:gccxml:"
eval "echo \"  +GCCXML_BASE:\${GCCXML_ROOT}\""
eval "echo \"  +PATH:\${GCCXML_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${GCCXML_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${GCCXML_ROOT}/include\""

echo "TOOL:boost_python:"
echo "  +BOOST_PYTHON_BASE:$BOOST_ROOT"
echo "  +LIBDIR:$BOOST_ROOT/lib"
echo "  +INCLUDE:$BOOST_ROOT/include"
echo "  +ELEMENTTREE_BASE:$ELEMENTTREE_ROOT"
echo "  +ELEMENTTREE_PYPATH=$ELEMENTTREE_ROOT/python$(echo $PYTHON_VERSION | cut -d. -f1,2)/site-packages"
echo "  +PYTHONPATH=$ELEMENTTREE_ROOT/lib/python$(echo $PYTHON_VERSION | cut -d. -f1,2)/site-packages"
echo "  +PYSTE_EXEC=$BOOST_ROOT/lib/python$(echo $PYTHON_VERSION | cut -d. -f1,2)/site-packages/Pyste/pyste.py"


echo "TOOL:bz2lib:"
eval "echo \"  +BZ2LIB_BASE:\${BZ2LIB_ROOT}\""
eval "echo \"  +PATH:\${BZ2LIB_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${BZ2LIB_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${BZ2LIB_ROOT}/include\""


echo "TOOL:pcre:"
eval "echo \"  +PCRE_BASE:\${PCRE_ROOT}\""
eval "echo \"  +PATH:\${PCRE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${PCRE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${PCRE_ROOT}/include\""


echo "TOOL:dcap:"
eval "echo \"  +DCAP_BASE:\${DCAP_ROOT}\""
eval "echo \"  +PATH:\${DCAP_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${DCAP_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${DCAP_ROOT}/include\""

echo "TOOL:rulechecker:"
echo "  +RULECHECKER_BASE:$RULECHECKER_ROOT"
echo "  +CLASSPATH:$RULECHECKER_ROOT:$CLASSPATH"
echo "  +RULECHECKER_PREPROCESS_EXT:i"
echo "  +RULECHECKER_VIOLATION_EXT:viol"


echo "TOOL:cppunit:"
eval "echo \"  +CPPUNIT_BASE:\${CPPUNIT_ROOT}\""
eval "echo \"  +PATH:\${CPPUNIT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${CPPUNIT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${CPPUNIT_ROOT}/include\""


echo "TOOL:qt:"
eval "echo \"  +QT_BASE:\${QT_ROOT}\""
eval "echo \"  +PATH:\${QT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${QT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${QT_ROOT}/include\""


echo "TOOL:soqt:"
eval "echo \"  +SOQT_BASE:\${SOQT_ROOT}\""
eval "echo \"  +PATH:\${SOQT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${SOQT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${SOQT_ROOT}/include\""

echo "TOOL:coin3d:"
eval "echo \"  +COIN3D_BASE:\${COIN_ROOT}\""
eval "echo \"  +PATH:\${COIN_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${COIN_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${COIN_ROOT}/include\""

echo "TOOL:jpeg:"
echo "  +JPEG_BASE:/usr"


echo "TOOL:simage:"
eval "echo \"  +SIMAGE_BASE:\${SIMAGE_ROOT}\""
eval "echo \"  +PATH:\${SIMAGE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${SIMAGE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${SIMAGE_ROOT}/include\""


echo "TOOL:openssl:"
eval "echo \"  +OPENSSL_BASE:\${OPENSSL_ROOT}\""
eval "echo \"  +PATH:\${OPENSSL_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${OPENSSL_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${OPENSSL_ROOT}/include\""

echo "TOOL:hippodraw:"
echo "  +HIPPODRAW_BASE:$HIPPODRAW_ROOT"
echo "  +LIBDIR:$HIPPODRAW_ROOT/lib"
echo "  +INCLUDE:$HIPPODRAW_ROOT/include/HippoDraw-$HIPPODRAW_VERSION"
echo "  +PATH:$PYTHON_ROOT/bin"


echo "TOOL:qutexmlrpc:"
eval "echo \"  +QUTEXMLRPC_BASE:\${QUTEXMLRPC_ROOT}\""
eval "echo \"  +PATH:\${QUTEXMLRPC_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${QUTEXMLRPC_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${QUTEXMLRPC_ROOT}/include\""


echo "TOOL:frontier_client:"
eval "echo \"  +FRONTIER_CLIENT_BASE:\${FRONTIER_CLIENT_ROOT}\""
eval "echo \"  +PATH:\${FRONTIER_CLIENT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${FRONTIER_CLIENT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${FRONTIER_CLIENT_ROOT}/include\""


echo "TOOL:genser:"
eval "echo \"  +GENSER_BASE:\${GENSER_ROOT}\""
eval "echo \"  +PATH:\${GENSER_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${GENSER_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${GENSER_ROOT}/include\""


echo "TOOL:pythia:"
eval "echo \"  +PYTHIA_BASE:\${PYTHIA_ROOT}\""
eval "echo \"  +PATH:\${PYTHIA_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${PYTHIA_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${PYTHIA_ROOT}/include\""


echo "TOOL:pythia6_227:"
eval "echo \"  +PYTHIA6_227_BASE:\${PYTHIA6_227_ROOT}\""
eval "echo \"  +PATH:\${PYTHIA6_227_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${PYTHIA6_227_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${PYTHIA6_227_ROOT}/include\""


echo "TOOL:fed9uutils:"
eval "echo \"  +FED9UUTILS_BASE:\${FED9UUTILS_ROOT}\""
eval "echo \"  +PATH:\${FED9UUTILS_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${FED9UUTILS_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${FED9UUTILS_ROOT}/include\""


echo "TOOL:icutils:"
eval "echo \"  +ICUTILS_BASE:\${ICUTILS_ROOT}\""
eval "echo \"  +PATH:\${ICUTILS_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${ICUTILS_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${ICUTILS_ROOT}/include\""


echo "TOOL:doxygen:"
eval "echo \"  +DOXYGEN_BASE:\${DOXYGEN_ROOT}\""
eval "echo \"  +PATH:\${DOXYGEN_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${DOXYGEN_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${DOXYGEN_ROOT}/include\""


echo "TOOL:meschach:"
eval "echo \"  +MESCHACH_BASE:\${MESCHACH_ROOT}\""
eval "echo \"  +PATH:\${MESCHACH_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${MESCHACH_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${MESCHACH_ROOT}/include\""

echo "TOOL:iguana:"
echo "  +IGUANA_BASE:$IGUANA_ROOT"

) > tools.conf
%install
mkdir %i/configurations/
cp tools.conf %i/configurations/tools-STANDALONE.conf
