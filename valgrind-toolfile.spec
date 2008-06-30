### RPM configuration valgrind-toolfile 2.4.0
## IMPORT scramtoolbox-common

Source: none
Requires: valgrind

%build
%install
mkdir -p %toolConfDir %toolBoxDir/TestingTools

cat << \EOF_valgrind_TOOLCONF_FRAGMENT > %toolConfDir/valgrind.conf
TOOL:valgrind
   +VALGRIND_BASE:${VALGRIND_ROOT}
   +PATH:${VALGRIND_ROOT}/bin
   +LIBDIR:${VALGRIND_ROOT}/lib
   +INCLUDE:${VALGRIND_ROOT}/include
EOF_valgrind_TOOLCONF_FRAGMENT

cat << \EOF_valgrind_TOOLFILE > %toolBoxDir/TestingTools/valgrind
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<client>
<environment name=VALGRIND_BASE>
The top of the valgrind distribution.
</environment>
</client>
<environment name=PATH value="$VALGRIND_BASE/bin" type=Runtime_path></environment>
</tool>
EOF_valgrind_TOOLFILE
%files
%toolBoxDir/TestingTools/valgrind
%toolConfDir/valgrind.conf
