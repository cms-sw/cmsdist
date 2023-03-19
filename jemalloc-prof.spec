# any "Requires" must come before "## INCLUDE jemalloc-common"
# to make sure they are declared before the "%prep" section defined there
Requires: libunwind
## INCLUDE jemalloc-common
### RPM external jemalloc-prof %{jemalloc_version}

%build
XOPTS=""
%ifarch aarch64
# set the huge page size to 16M ( log2(16M)=24 ) on ARMv8
XOPTS="--with-lg-hugepage=24"
%endif

export CXXFLAGS=-I$LIBUNWIND_ROOT/include
export CFLAGS=-I$LIBUNWIND_ROOT/include
export LDFLAGS=-L$LIBUNWIND_ROOT/lib

./autogen.sh ${XOPTS} \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --enable-prof \
  --enable-prof-libunwind \
  --prefix %{i}
