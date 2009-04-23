### RPM configuration uuid-toolfile 1.38
## IMPORT scramtoolbox-common

Source: none
Requires: uuid

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_uuid_TOOLCONF_FRAGMENT > %toolConfDir/uuid.conf
TOOL:uuid
   +UUID_BASE:${UUID_ROOT}
   +PATH:${UUID_ROOT}/bin
   +LIBDIR:${UUID_ROOT}/lib
   +INCLUDE:${UUID_ROOT}/include
EOF_uuid_TOOLCONF_FRAGMENT

cat << \EOF_uuid_TOOLFILE > %toolBoxDir/General/uuid
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<lib name=uuid>
<client>
<environment name=UUID_BASE>
The top of the UUID distribution.
</environment>
<environment name=LIBDIR default="$UUID_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$UUID_BASE/include"></environment>
</client>
<external ref=sockets version=1.0 >
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<architecture name=win32>
<environment name=PATH value="$LIBDIR:$PATH">
Specific because of a problem with existing system uui.dll
</environment>
</architecture>
</tool>
EOF_uuid_TOOLFILE
%files
%toolBoxDir/General/uuid
%toolConfDir/uuid.conf
