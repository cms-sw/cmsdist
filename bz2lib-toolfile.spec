### RPM configuration bz2lib-toolfile 1.0.2
## IMPORT scramtoolbox-common

Source: none
Requires: bz2lib

%build
%install
%define toolfilePath %toolBoxDir/General
mkdir -p %toolConfDir %toolfilePath

cat << \EOF_bz2lib_TOOLCONF_FRAGMENT > %toolConfDir/bz2lib.conf
TOOL:bz2lib
   +BZ2LIB_BASE:${BZ2LIB_ROOT}
   +PATH:${BZ2LIB_ROOT}/bin
   +LIBDIR:${BZ2LIB_ROOT}/lib
   +INCLUDE:${BZ2LIB_ROOT}/include
EOF_bz2lib_TOOLCONF_FRAGMENT

cat << \EOF_bz2lib_TOOLFILE > %toolfilePath/bz2lib
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://sources.redhat.com/bzip2/"></info>
<architecture name=macosx>
<lib name=bz2>
</architecture>
<architecture name=osx>
<lib name=bz2>
</architecture>
<architecture name=sl>
<lib name=bz2>
</architecture>
<architecture name=win>
<lib name=libbz2>
</architecture>
<client>
<environment name=BZ2LIB_BASE>
The top of the BZ2LIB distribution.
</environment>
<environment name=LIBDIR default="$BZ2LIB_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$BZ2LIB_BASE/include"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</tool>
EOF_bz2lib_TOOLFILE
%files
%toolfilePath/bz2lib
%toolConfDir/bz2lib.conf
