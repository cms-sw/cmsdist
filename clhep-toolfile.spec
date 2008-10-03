### RPM configuration clhep-toolfile 1.9.2.2
## IMPORT scramtoolbox-common

Source: none
Requires: clhep

%build
%install
%define toolfilePath %toolBoxDir/General
mkdir -p %toolConfDir %toolfilePath

cat << \EOF_clhep_TOOLCONF_FRAGMENT > %toolConfDir/clhep.conf
TOOL:clhep
   +CLHEP_BASE:${CLHEP_ROOT}
   +PATH:${CLHEP_ROOT}/bin
   +LIBDIR:${CLHEP_ROOT}/lib
   +INCLUDE:${CLHEP_ROOT}/include
EOF_clhep_TOOLCONF_FRAGMENT

cat << \EOF_clhep_TOOLFILE > %toolfilePath/clhep
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://cern.ch/clhep"></info>
<architecture name=macosx>
<lib name=CLHEP-Cast-1.9.2.2>
<lib name=CLHEP-Evaluator-1.9.2.2>
<lib name=CLHEP-Exceptions-1.9.2.2>
<lib name=CLHEP-GenericFunctions-1.9.2.2>
<lib name=CLHEP-Geometry-1.9.2.2>
<lib name=CLHEP-Matrix-1.9.2.2>
<lib name=CLHEP-Random-1.9.2.2>
<lib name=CLHEP-RandomObjects-1.9.2.2>
<lib name=CLHEP-RefCount-1.9.2.2>
<lib name=CLHEP-Vector-1.9.2.2>
</architecture>
<architecture name=osx>
<lib name=CLHEP-Cast-1.9.2.2>
<lib name=CLHEP-Evaluator-1.9.2.2>
<lib name=CLHEP-Exceptions-1.9.2.2>
<lib name=CLHEP-GenericFunctions-1.9.2.2>
<lib name=CLHEP-Geometry-1.9.2.2>
<lib name=CLHEP-Matrix-1.9.2.2>
<lib name=CLHEP-Random-1.9.2.2>
<lib name=CLHEP-RandomObjects-1.9.2.2>
<lib name=CLHEP-RefCount-1.9.2.2>
<lib name=CLHEP-Vector-1.9.2.2>
</architecture>
<architecture name=rh>
<lib name=CLHEP-Cast-1.9.2.2>
<lib name=CLHEP-Evaluator-1.9.2.2>
<lib name=CLHEP-Exceptions-1.9.2.2>
<lib name=CLHEP-GenericFunctions-1.9.2.2>
<lib name=CLHEP-Geometry-1.9.2.2>
<lib name=CLHEP-Matrix-1.9.2.2>
<lib name=CLHEP-Random-1.9.2.2>
<lib name=CLHEP-RandomObjects-1.9.2.2>
<lib name=CLHEP-RefCount-1.9.2.2>
<lib name=CLHEP-Vector-1.9.2.2>
</architecture>
<architecture name=cel>
<lib name=CLHEP-Cast-1.9.2.2>
<lib name=CLHEP-Evaluator-1.9.2.2>
<lib name=CLHEP-Exceptions-1.9.2.2>
<lib name=CLHEP-GenericFunctions-1.9.2.2>
<lib name=CLHEP-Geometry-1.9.2.2>
<lib name=CLHEP-Matrix-1.9.2.2>
<lib name=CLHEP-Random-1.9.2.2>
<lib name=CLHEP-RandomObjects-1.9.2.2>
<lib name=CLHEP-RefCount-1.9.2.2>
<lib name=CLHEP-Vector-1.9.2.2>
</architecture>
<architecture name=sl>
<lib name=CLHEP-Cast-1.9.2.2>
<lib name=CLHEP-Evaluator-1.9.2.2>
<lib name=CLHEP-Exceptions-1.9.2.2>
<lib name=CLHEP-GenericFunctions-1.9.2.2>
<lib name=CLHEP-Geometry-1.9.2.2>
<lib name=CLHEP-Matrix-1.9.2.2>
<lib name=CLHEP-Random-1.9.2.2>
<lib name=CLHEP-RandomObjects-1.9.2.2>
<lib name=CLHEP-RefCount-1.9.2.2>
<lib name=CLHEP-Vector-1.9.2.2>
</architecture>
<architecture name=win32>
<lib name=libCLHEP-Cast-1.9.2.2.lib>
<lib name=libCLHEP-Evaluator-1.9.2.2.lib>
<lib name=libCLHEP-Exceptions-1.9.2.2.lib>
<lib name=libCLHEP-GenericFunctions-1.9.2.2.lib>
<lib name=libCLHEP-Geometry-1.9.2.2.lib>
<lib name=libCLHEP-Matrix-1.9.2.2.lib>
<lib name=libCLHEP-Random-1.9.2.2.lib>
<lib name=libCLHEP-RandomObjects-1.9.2.2.lib>
<lib name=libCLHEP-RefCount-1.9.2.2.lib>
<lib name=libCLHEP-Vector-1.9.2.2.lib>
</architecture>
<client>
<environment name=CLHEP_BASE>
The top of the standard CLHEP distribution.
</environment>
<environment name=LIBDIR default="$CLHEP_BASE/lib" type=lib>
The Library location for the CLHEP distribution
</environment>
<environment name=INCLUDE default="$CLHEP_BASE/include">
The header file location for the CLHEP distribution
</environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</tool>
EOF_clhep_TOOLFILE
%files
%toolfilePath/clhep
%toolConfDir/clhep.conf
