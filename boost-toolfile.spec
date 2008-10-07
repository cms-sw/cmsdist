### RPM configuration boost-toolfile 1.33.1
## IMPORT scramtoolbox-common

Source: none
Requires: boost

%build
%install
%define toolfilePath %toolBoxDir/General
mkdir -p %toolConfDir %toolfilePath

cat << \EOF_boost_TOOLCONF_FRAGMENT > %toolConfDir/boost.conf
TOOL:boost
   +BOOST_BASE:${BOOST_ROOT}
   +PATH:${BOOST_ROOT}/bin
   +LIBDIR:${BOOST_ROOT}/lib
   +INCLUDE:${BOOST_ROOT}/include
EOF_boost_TOOLCONF_FRAGMENT

cat << \EOF_boost_TOOLFILE > %toolfilePath/boost
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://www.boost.org"></info>
<client>
<environment name=BOOST_BASE>
The top of the Boost distribution.
</environment>
<environment name=LIBDIR default="$BOOST_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$BOOST_BASE/include/boost-1_33_1"></environment>
</client>
<external ref=sockets version=1.0 >
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<environment name=PYTHONPATH value="$BOOST_BASE/lib/python2.4/site-packages" type=Runtime_path></environment>
<architecture name=win32>
<environment name=PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
</tool>
EOF_boost_TOOLFILE
%files
%toolfilePath/boost
%toolConfDir/boost.conf
