### RPM configuration root-toolfile 5.06.11a
## IMPORT scramtoolbox-common

Source: none
Requires: root

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_root_TOOLCONF_FRAGMENT > %toolConfDir/root.conf
TOOL:root
   +ROOT_BASE:${ROOT_ROOT}
   +PATH:${ROOT_ROOT}/bin
   +LIBDIR:${ROOT_ROOT}/lib
   +INCLUDE:${ROOT_ROOT}/include
EOF_root_TOOLCONF_FRAGMENT

cat << \EOF_root_TOOLFILE > %toolBoxDir/General/root
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://root.cern.ch/root/"></info>
<architecture name=macosx>
<lib name=Cint>
<lib name=Core>
<lib name=Tree>
</architecture>
<architecture name=rh>
<lib name=Cint>
<lib name=Core>
<lib name=Tree>
</architecture>
<architecture name=cel>
<lib name=Cint>
<lib name=Core>
<lib name=Tree>
</architecture>
<architecture name=sl>
<lib name=Cint>
<lib name=Core>
<lib name=Tree>
</architecture>
<architecture name=osx>
<lib name=Cint>
<lib name=Core>
<lib name=Tree>
</architecture>
<architecture name=win>
<lib name=libCint>
<lib name=libCore>
<lib name=libTree>
</architecture>
<client>
<environment name=ROOT_BASE>
Base of the ROOT analysis package.
</environment>
<environment name=LIBDIR default="$ROOT_BASE/root/lib" type=lib>
Location of ROOT libraries.
</environment>
<environment name=INCLUDE default="$ROOT_BASE/root/include">
Location of ROOT include files.
</environment>
<environment name=ROOTSYS default="$ROOT_BASE/root" type=Runtime></environment>
</client>
<environment name=PATH value="$ROOTSYS/bin" type=Runtime_path></environment>
<architecture name=macosx>
<environment name=PYTHONPATH value="$ROOTSYS/lib" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
<architecture name=rh>
<environment name=PYTHONPATH value="$ROOTSYS/lib" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
<architecture name=cel>
<environment name=PYTHONPATH value="$ROOTSYS/lib" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
<architecture name=sl>
<environment name=PYTHONPATH value="$ROOTSYS/lib" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
<architecture name=osx>
<environment name=LDFLAGS value="-u _G__cpp_setup_initializerG__Tree"></environment>
<environment name=PYTHONPATH value="$ROOTSYS/lib" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
<architecture name=win>
<environment name=PYTHONPATH value="$ROOTSYS/bin" type=Runtime_path></environment>
<environment name=LD_LIBRARY_PATH value="$ROOTSYS/bin" type=Runtime_path></environment>
</architecture>
</tool>
EOF_root_TOOLFILE
%files
%toolBoxDir/General/root
%toolConfDir/root.conf
