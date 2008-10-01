### RPM configuration gccxml-toolfile 0.6.0_patch3
## IMPORT scramtoolbox-common

Source: none

%build
%install
echo %toolConfDir
mkdir -p %toolBoxDir/General %toolConfDir

cat << \EOF_gccxml_TOOLCONF_FRAGMENT > %toolConfDir/gccxml.conf
TOOL:gccxml
   +GCCXML_BASE:${GCCXML_ROOT}
   +PATH:${GCCXML_ROOT}/bin
   +LIBDIR:${GCCXML_ROOT}/lib
   +INCLUDE:${GCCXML_ROOT}/include
EOF_gccxml_TOOLCONF_FRAGMENT

cat << \EOF_gccxml_TOOLFILE > %toolBoxDir/General/gccxml
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<client>
<environment name=GCCXML_BASE>
The top of the gccxml distribution.
</environment>
</client>
<architecture name=macosx>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=osx>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=rh>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=cel>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=sl>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=win>
<environment name=PATH value="$GCCXML_BASE/bin" type=Runtime_path></environment>
</architecture>
</tool>
EOF_gccxml_TOOLFILE

%files
%toolBoxDir/General/gccxml
%toolConfDir/gccxml.conf
