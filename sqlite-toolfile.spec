### RPM configuration sqlite-toolfile 3.3.5
## IMPORT scramtoolbox-common

Source: none
Requires: sqlite

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_sqlite_TOOLCONF_FRAGMENT > %toolConfDir/sqlite.conf
TOOL:sqlite
   +SQLITE_BASE:${SQLITE_ROOT}
   +PATH:${SQLITE_ROOT}/bin
   +LIBDIR:${SQLITE_ROOT}/lib
   +INCLUDE:${SQLITE_ROOT}/include
EOF_sqlite_TOOLCONF_FRAGMENT

cat << \EOF_sqlite_TOOLFILE > %toolBoxDir/General/sqlite
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<lib name=sqlite3>
<client>
<environment name=SQLITE_BASE></environment>
<environment name=LIBDIR default="$SQLITE_BASE/lib" type=lib></environment>
<environment name=BINDIR default="$SQLITE_BASE/bin"></environment>
<environment name=INCLUDE default="$SQLITE_BASE/include"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<environment name=PATH value="$BINDIR" type=Runtime_path></environment>
</tool>
EOF_sqlite_TOOLFILE
%files
%toolBoxDir/General/sqlite
%toolConfDir/sqlite.conf
