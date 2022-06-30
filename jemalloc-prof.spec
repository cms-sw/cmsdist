# any "Requires" must come before "## INCLUDE jemalloc-common"
# to make sure they are declared before the "%prep" section defined there
Requires: libunwind
## INCLUDE jemalloc-common
### RPM external jemalloc-prof %{jemalloc_version}

%build
export CXXFLAGS=-I$LIBUNWIND_ROOT/include
export CFLAGS=-I$LIBUNWIND_ROOT/include
export LDFLAGS=-L$LIBUNWIND_ROOT/lib

./autogen.sh \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --enable-prof \
  --enable-prof-libunwind \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
