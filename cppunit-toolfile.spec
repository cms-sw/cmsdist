### RPM configuration cppunit-toolfile 1.10.2
## IMPORT scramtoolbox-common

Source: none
Requires: cppunit

%build
%install
mkdir -p %toolConfDir %toolBoxDir/TestingTools

cat << \EOF_cppunit_TOOLCONF_FRAGMENT > %toolConfDir/cppunit.conf
TOOL:cppunit
   +CPPUNIT_BASE:${CPPUNIT_ROOT}
   +PATH:${CPPUNIT_ROOT}/bin
   +LIBDIR:${CPPUNIT_ROOT}/lib
   +INCLUDE:${CPPUNIT_ROOT}/include
EOF_cppunit_TOOLCONF_FRAGMENT

cat << \EOF_cppunit_TOOLFILE > %toolBoxDir/TestingTools/cppunit
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<architecture name=macosx>
<lib name=cppunit>
</architecture>
<architecture name=osx>
<lib name=cppunit>
</architecture>
<architecture name=sl>
<lib name=cppunit>
</architecture>
<architecture name=win>
<lib name=cppunit_dll>
</architecture>
<client>
<environment name=CPPUNIT_BASE>
The top of the CPpUnit distribution.
</environment>
<environment name=LIBDIR default="$CPPUNIT_BASE/lib" type=lib>
Location of CppUnit libraries.
</environment>
<environment name=INCLUDE default="$CPPUNIT_BASE/include">
Location of CppUnit include files.
</environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<architecture name=win>
<environment name=PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
</tool>
EOF_cppunit_TOOLFILE
%files
%toolBoxDir/TestingTools/cppunit
%toolConfDir/cppunit.conf
