ROOT_GX11_LIB=GX11
[ $(uname -s) = "Darwin" ] && ROOT_GX11_LIB=GCocoa
export ROOT_GX11_LIB

export GENREFLEX_FAILES_ON_WARNS=--fail_on_warnings
if [ "$ROOT_CXXMODULES" = "1" ] ; then
  export GENREFLEX_FAILES_ON_WARNS=-failOnWarnings
fi
