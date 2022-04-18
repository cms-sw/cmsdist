export CXXMODULE_DATA=""
if [ "${ROOT_CXXMODULES}" = "1" ] ; then
  export CXXMODULE_DATA='<flags ROOTCLING_ARGS="-moduleMapFile=$(FMT_BASE)/include/module.modulemap"/>'
fi
