### RPM configuration python-toolfile 2.4.2
## IMPORT scramtoolbox-common

Source: none
Requires: python

%build
%install
mkdir -p %toolConfDir %toolBoxDir/General

cat << \EOF_python_TOOLCONF_FRAGMENT > %toolConfDir/python.conf
TOOL:python
   +PYTHON_BASE:${PYTHON_ROOT}
   +PATH:${PYTHON_ROOT}/bin
   +LIBDIR:${PYTHON_ROOT}/lib
   +INCLUDE:${PYTHON_ROOT}/include
EOF_python_TOOLCONF_FRAGMENT

cat << \EOF_python_TOOLFILE > %toolBoxDir/General/python
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<architecture name=macosx>
<lib name=python2.4>
</architecture>
<architecture name=osx>
<lib name=python2.4>
</architecture>
<architecture name=sl>
<lib name=python2.4>
</architecture>
<architecture name=win>
<lib name=python24>
</architecture>
<client>
<environment name=PYTHON_BASE>
The top of the Python distribution.
</environment>
<environment name=INCLUDE default="$PYTHON_BASE/include/python2.4"></environment>
<environment name=LIBDIR default="$PYTHON_BASE/lib" type=lib></environment>
<architecture name=macosx>
<environment name=PATH value="$PYTHON_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=osx>
<environment name=PATH value="$PYTHON_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=sl>
<environment name=PATH value="$PYTHON_BASE/bin" type=Runtime_path></environment>
</architecture>
<architecture name=win>
<environment name=PATH value="$PYTHON_BASE/" type=Runtime_path></environment>
</architecture>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
</tool>

EOF_python_TOOLFILE
%files
%toolBoxDir/General/python
%toolConfDir/python.conf
