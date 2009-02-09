### RPM configuration pcre-toolfile 4.4
## IMPORT scramtoolbox-common

Source: none
Requires: pcre

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_pcre_TOOLCONF_FRAGMENT > %toolConfDir/pcre.conf
TOOL:pcre
   +PCRE_BASE:${PCRE_ROOT}
   +PATH:${PCRE_ROOT}/bin
   +LIBDIR:${PCRE_ROOT}/lib
   +INCLUDE:${PCRE_ROOT}/include
EOF_pcre_TOOLCONF_FRAGMENT

cat << \EOF_pcre_TOOLFILE > %toolBoxDir/General/pcre
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://www.pcre.org"></info>
<architecture name=macosx>
<lib name=pcre>
</architecture>
<architecture name=osx>
<lib name=pcre>
</architecture>
<architecture name=sl>
<lib name=pcre>
</architecture>
<architecture name=win>
<lib name=libpcre>
</architecture>
<client>
<environment name=PCRE_BASE>
The top of the PCRE distribution.
</environment>
<environment name=LIBDIR default="$PCRE_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$PCRE_BASE/include"></environment>
<environment name=BINDIR default="$PCRE_BASE/bin"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<architecture name=win>
<environment name=PATH value="$BINDIR" type=Runtime_path></environment>
</architecture>
</tool>
EOF_pcre_TOOLFILE
%files
%toolBoxDir/General/pcre
%toolConfDir/pcre.conf
