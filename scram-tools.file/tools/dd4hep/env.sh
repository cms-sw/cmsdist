export GCC_GLIBCXX_VERSION=$(gcc -dumpversion | tr '.' '0')
export CXXMODULE_DATA=""
if [ "${ROOT_CXXMODULES}" = "1" ] ; then
  export CXXMODULE_DATA='<flags ROOTCLING_ARGS="-moduleMapFile=$(DD4HEP_BASE)/include/module.modulemap"/>'
fi
