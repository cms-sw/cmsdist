### RPM configuration zlib-toolfile 1.1.4
## IMPORT scramtoolbox-common

Source: none
Requires: zlib

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_zlib_TOOLCONF_FRAGMENT > %toolConfDir/zlib.conf
TOOL:zlib
   +ZLIB_BASE:${ZLIB_ROOT}
   +PATH:${ZLIB_ROOT}/bin
   +LIBDIR:${ZLIB_ROOT}/lib
   +INCLUDE:${ZLIB_ROOT}/include
EOF_zlib_TOOLCONF_FRAGMENT

cat << \EOF_zlib_TOOLFILE > %toolBoxDir/General/zlib
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://www.gzip.org/zlib/"></info>
<architecture name=macosx>
<lib name=z>
</architecture>
<architecture name=osx>
<lib name=z>
</architecture>
<architecture name=sl>
<lib name=z>
</architecture>
<architecture name=win>
<lib name=zlib>
</architecture>
<client>
<environment name=ZLIB_BASE></environment>
<environment name=LIBDIR default="$ZLIB_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$ZLIB_BASE/include"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<architecture name=win>
<environment name=PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
</tool>
EOF_zlib_TOOLFILE
%files
%toolBoxDir/General/zlib
%toolConfDir/zlib.conf
