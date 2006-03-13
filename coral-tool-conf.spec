
### RPM lcg coral-tool-conf 40
Source0: none

Requires: gcc

Requires: oracle
Requires: sqlite
Requires: mysql
Requires: frontier_client
Requires: expat
Requires: xerces-c
Requires: cppunit
Requires: oval
Requires: qmtest
Requires: valgrind
Requires: seal
Requires: uuid
Requires: boost
Requires: pcre
%prep
%build
(echo "ARCHITECTURE:%{cmsplatf}"
 echo "SCRAM_BASEPATH:%{instroot}/external"

%define is_arch_slc3_ia32_gcc3 %(if [ `echo "%{cmsplatf}" | sed -e 's/\(slc3_ia32_gcc3\)/\1/'` = "%{cmsplatf}" ]; then echo true; else echo %%{nil}; fi)
%if %is_arch_slc3_ia32_gcc3
%if "%{?use_system_gcc:set}" == "set"
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:/none"
       echo "  +CC:$(which gcc)"
       echo "  +CXX:$(which c++)"
       echo "  +PATH:/none"  # useless, toolbox says value=""
       echo "  +LD_LIBRARY_PATH:/none" # useless, toolbox says value=""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$(which g77)"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-set"
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:$GCC_ROOT"
eval       "echo \"  +CC:$CCACHE_ROOT/bin/gcc\""
eval       "echo \"  +CXX:$CCACHE_ROOT/bin/c++\""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-" 
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:$GCC_ROOT"
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif

%endif 

%define is_arch_slc3_amd64_gcc3 %(if [ `echo "%{cmsplatf}" | sed -e 's/\(slc3_amd64_gcc3\)/\1/'` = "%{cmsplatf}" ]; then echo true; else echo %%{nil}; fi)
%if %is_arch_slc3_amd64_gcc3
%if "%{?use_system_gcc:set}" == "set"
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:/none"
       echo "  +CC:$(which gcc)"
       echo "  +CXX:$(which c++)"
       echo "  +PATH:/none"  # useless, toolbox says value=""
       echo "  +LD_LIBRARY_PATH:/none" # useless, toolbox says value=""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$(which g77)"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-set"
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:$GCC_ROOT"
eval       "echo \"  +CC:$CCACHE_ROOT/bin/gcc\""
eval       "echo \"  +CXX:$CCACHE_ROOT/bin/c++\""
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif
%if "%{?use_system_gcc:set}-%{?use_ccache:set}" == "-" 
       echo "TOOL:gcc3:"
       echo "  +GCC_BASE:$GCC_ROOT"
       echo "TOOL:g77gcc3:"
       echo "  +FC:$GCC_ROOT/bin/g77"
%endif

%endif 

%define is_arch_win32_vc71 %(if [ `echo "%{cmsplatf}" | sed -e 's/\(win32_vc71\)/\1/'` = "%{cmsplatf}" ]; then echo true; else echo %%{nil}; fi)
%if %is_arch_win32_vc71

echo "TOOL:rx:"
eval "echo \"  +RX_BASE:\${RX_ROOT}\""
eval "echo \"  +PATH:\${RX_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${RX_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${RX_ROOT}/include\""

%endif 

echo "TOOL:oracle:"
echo "  +ORACLE_BASE:$ORACLE_ROOT"
echo "  +PATH:$ORACLE_ROOT/bin"
echo "  +LIBDIR:$ORACLE_ROOT/lib"
echo "  +INCLUDE:$ORACLE_ROOT/include"
echo "  +TNS_ADMIN:$ORACLE_ROOT/admin"


echo "TOOL:sqlite:"
eval "echo \"  +SQLITE_BASE:\${SQLITE_ROOT}\""
eval "echo \"  +PATH:\${SQLITE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${SQLITE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${SQLITE_ROOT}/include\""

echo "TOOL:mysql:"
eval "echo \"  +MYSQL_BASE:\${MYSQL_ROOT}\""
eval "echo \"  +PATH:\${MYSQL_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${MYSQL_ROOT}/lib/mysql\""
eval "echo \"  +INCLUDE:\${MYSQL_ROOT}/include/mysql\""


echo "TOOL:frontier_client:"
eval "echo \"  +FRONTIER_CLIENT_BASE:\${FRONTIER_CLIENT_ROOT}\""
eval "echo \"  +PATH:\${FRONTIER_CLIENT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${FRONTIER_CLIENT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${FRONTIER_CLIENT_ROOT}/include\""


echo "TOOL:expat:"
eval "echo \"  +EXPAT_BASE:\${EXPAT_ROOT}\""
eval "echo \"  +PATH:\${EXPAT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${EXPAT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${EXPAT_ROOT}/include\""

echo "TOOL:xerces-c:"
eval "echo \"  +XERCESC_BASE:\${XERCES_C_ROOT}\""
eval "echo \"  +XERCES_C_BASE:\${XERCES_C_ROOT}\""
eval "echo \"  +PATH:\${XERCES_C_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${XERCES_C_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${XERCES_C_ROOT}/include\""


echo "TOOL:cppunit:"
eval "echo \"  +CPPUNIT_BASE:\${CPPUNIT_ROOT}\""
eval "echo \"  +PATH:\${CPPUNIT_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${CPPUNIT_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${CPPUNIT_ROOT}/include\""


echo "TOOL:oval:"
eval "echo \"  +OVAL_BASE:\${OVAL_ROOT}\""
eval "echo \"  +PATH:\${OVAL_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${OVAL_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${OVAL_ROOT}/include\""


echo "TOOL:qmtest:"
eval "echo \"  +QMTEST_BASE:\${QMTEST_ROOT}\""
eval "echo \"  +PATH:\${QMTEST_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${QMTEST_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${QMTEST_ROOT}/include\""


echo "TOOL:valgrind:"
eval "echo \"  +VALGRIND_BASE:\${VALGRIND_ROOT}\""
eval "echo \"  +PATH:\${VALGRIND_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${VALGRIND_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${VALGRIND_ROOT}/include\""

echo "TOOL:seal:"
echo "  +SEAL_BASE:$SEAL_ROOT"


echo "TOOL:uuid:"
eval "echo \"  +UUID_BASE:\${UUID_ROOT}\""
eval "echo \"  +PATH:\${UUID_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${UUID_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${UUID_ROOT}/include\""


echo "TOOL:boost:"
eval "echo \"  +BOOST_BASE:\${BOOST_ROOT}\""
eval "echo \"  +PATH:\${BOOST_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${BOOST_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${BOOST_ROOT}/include\""


echo "TOOL:pcre:"
eval "echo \"  +PCRE_BASE:\${PCRE_ROOT}\""
eval "echo \"  +PATH:\${PCRE_ROOT}/bin\""
eval "echo \"  +LIBDIR:\${PCRE_ROOT}/lib\""
eval "echo \"  +INCLUDE:\${PCRE_ROOT}/include\""

) > tools.conf
%install
mkdir %i/configurations/
cp tools.conf %i/configurations/tools-STANDALONE.conf
