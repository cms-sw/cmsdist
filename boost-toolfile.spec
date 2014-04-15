### RPM external boost-toolfile 1.0
Requires: boost
%prep

%build

%install

mkdir -p %i/etc/scram.d
# boost toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost.xml
<tool name="boost" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_THREAD_LIB@"/>
  <lib name="@BOOST_SIGNALS_LIB@"/>
  <lib name="@BOOST_DATE_TIME_LIB@"/>
  <client>
    <environment name="BOOST_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$BOOST_BASE/lib"/>
    <environment name="INCLUDE" default="$BOOST_BASE/include"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$BOOST_BASE/include" type="path"/>
  <flags CPPDEFINES="BOOST_SPIRIT_THREADSAFE PHOENIX_THREADSAFE"/>
  <use name="sockets"/>
</tool>
EOF_TOOLFILE

# boost_filesystem toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_filesystem.xml
<tool name="boost_filesystem" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_FILESYSTEM_LIB@"/>
  <use name="boost_system"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

# boost_system toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_system.xml
<tool name="boost_system" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_SYSTEM_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

# boost_program_options toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_program_options.xml
<tool name="boost_program_options" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_PROGRAM_OPTIONS_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

# boost_python toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_python.xml
<tool name="boost_python" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_PYTHON_LIB@"/>
  <client>
    <environment name="BOOST_PYTHON_BASE" default="@TOOL_ROOT@"/>
    <environment name="PYSTE_EXEC" default="$BOOST_PYTHON_BASE/lib/python@PYTHONV@/site-packages/Pyste/pyste.py"/>
    <environment name="LIBDIR" default="$BOOST_PYTHON_BASE/lib"/>
    <environment name="INCLUDE" default="$BOOST_PYTHON_BASE/include"/>
  </client>
  <use name="gccxml"/>
  <use name="python"/>
</tool>
EOF_TOOLFILE

# boost_regex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_regex.xml
<tool name="boost_regex" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_REGEX_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

# boost_signals toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_signals.xml
<tool name="boost_signals" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_SIGNALS_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_serialization.xml
<tool name="boost_serialization" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_SERIALIZATION_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_iostreams.xml
<tool name="boost_iostreams" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <lib name="@BOOST_IOSTREAMS_LIB@"/>
  <use name="boost"/>
</tool>
EOF_TOOLFILE

# boost_header toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/boost_header.xml
<tool name="boost_header" version="@TOOL_VERSION@">
  <info url="http://www.boost.org"/>
  <client>
    <environment name="BOOSTHEADER_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" default="$BOOSTHEADER_BASE/include"/>
  </client>
</tool>
EOF_TOOLFILE

case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
getLibName()
{
  libname=`find $BOOST_ROOT/lib -name "libboost_$1.$so" -exec basename {} \;`
  echo $libname | sed -e 's|[.][^-]*$||;s|^lib||'
}

export BOOST_THREAD_LIB=`getLibName thread`
export BOOST_SIGNALS_LIB=`getLibName signals`
export BOOST_FILESYSTEM_LIB=`getLibName filesystem`
export BOOST_DATE_TIME_LIB=`getLibName date_time`
export BOOST_SYSTEM_LIB=`getLibName system`
export BOOST_PROGRAM_OPTIONS_LIB=`getLibName program_options`
export BOOST_PYTHON_LIB=`getLibName python`
export BOOST_REGEX_LIB=`getLibName regex`
export BOOST_SERIALIZATION_LIB=`getLibName serialization`
export BOOST_IOSTREAMS_LIB=`getLibName iostream`
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
