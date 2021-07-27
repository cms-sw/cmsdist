source ${SCRAM_TOOLS_BIN_DIR}/os_libdir.sh
export CXXMODULE_DATA=""
if [ "${ROOT_CXXMODULES}" = "1" ] ; then
  export CXXMODULE_DATA='<runtime name="CLING_PREBUILT_MODULE_PATH" value="$CMSSW_BASE/lib/$SCRAM_ARCH" type="path"/>'
fi
