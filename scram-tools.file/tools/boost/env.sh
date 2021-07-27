so=so
[ "$(uname -s)" = "Darwin" ] && so=dylib
getLibName()
{
  libname=`find ${TOOL_ROOT}/lib -name "libboost_$1.$so" -follow -exec basename {} \;`
  echo $libname | sed -e 's|[.][^-]*$||;s|^lib||'
}
PYLIB=`ls ${TOOL_ROOT}/lib | grep boost_python | head -1`;PYLIB=${PYLIB%\.${so}};PYLIB=${PYLIB#lib}

export BOOST_THREAD_LIB=`getLibName thread`
export BOOST_CHRONO_LIB=`getLibName chrono`
export BOOST_FILESYSTEM_LIB=`getLibName filesystem`
export BOOST_DATE_TIME_LIB=`getLibName date_time`
export BOOST_SYSTEM_LIB=`getLibName system`
export BOOST_PROGRAM_OPTIONS_LIB=`getLibName program_options`
export BOOST_PYTHON_LIB=$PYLIB
export BOOST_REGEX_LIB=`getLibName regex`
export BOOST_SERIALIZATION_LIB=`getLibName serialization`
export BOOST_IOSTREAMS_LIB=`getLibName iostreams`
export BOOST_MPI_LIB=`getLibName mpi`

export CXXMODULE_DATA=""
if [ "${ROOT_CXXMODULES}" = "1" ] ; then
  export CXXMODULE_DATA='<flags ROOTCLING_ARGS="-moduleMapFile=$(BOOSTHEADER_BASE)/include/boost/boost.modulemap"/>'
fi
