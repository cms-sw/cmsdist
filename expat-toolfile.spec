### RPM configuration expat-toolfile 1.95.8
## IMPORT scramtoolbox-common

Source: none
Requires: expat

%build
%install
mkdir -p %toolConfDir %toolBoxDir/XMLTools

cat << \EOF_expat_TOOLCONF_FRAGMENT > %toolConfDir/expat.conf
TOOL:expat
   +EXPAT_BASE:${EXPAT_ROOT}
   +PATH:${EXPAT_ROOT}/bin
   +LIBDIR:${EXPAT_ROOT}/lib
   +INCLUDE:${EXPAT_ROOT}/include
EOF_expat_TOOLCONF_FRAGMENT

cat << \EOF_expat_TOOLFILE > %toolBoxDir/XMLTools/expat
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<architecture name=macosx>
<lib name=expat>
</architecture>
<architecture name=osx>
<lib name=expat>
</architecture>
<architecture name=rh>
<lib name=expat>
</architecture>
<architecture name=cel>
<lib name=expat>
</architecture>
<architecture name=sl>
<lib name=expat>
</architecture>
<architecture name=win>
<lib name=libexpat>
</architecture>
<client>
<environment name=EXPAT_BASE></environment>
<environment name=LIBDIR default="$EXPAT_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$EXPAT_BASE/include"></environment>
<environment name=BINDIR default="$EXPAT_BASE/bin"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<environment name=PATH value="$BINDIR" type=Runtime_path></environment>
</tool>
EOF_expat_TOOLFILE
%files
%toolBoxDir/XMLTools/expat
%toolConfDir/expat.conf
