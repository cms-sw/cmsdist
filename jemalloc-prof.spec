# any "Requires" must come before "## INCLUDE jemalloc-common"
# to make sure they are declared before the "%prep" section defined there
Requires: libunwind
## INCLUDE jemalloc-common
### RPM external jemalloc-prof %{jemalloc_version}
%define autogen_opts --enable-prof --enable-prof-libunwind
%define PreBuild \
  export CXXFLAGS=-I$LIBUNWIND_ROOT/include \
  export CFLAGS=-I$LIBUNWIND_ROOT/include \
  export LDFLAGS=-L$LIBUNWIND_ROOT/lib
