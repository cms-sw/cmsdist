if [ $(uname -s) = "Darwin" ] ; then
  export OS_RUNTIME_LDPATH_NAME="DYLD_LIBRARY_PATH"
else
  export OS_RUNTIME_LDPATH_NAME="LD_LIBRARY_PATH"
fi

