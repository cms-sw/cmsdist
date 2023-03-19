## INCLUDE jemalloc-common
### RPM external jemalloc %{jemalloc_version}

%build
XOPTS=""
%ifarch aarch64
# set the huge page size to 16M ( log2(16M)=24 ) on ARMv8
XOPTS="--with-lg-hugepage=24"
%endif

./autogen.sh ${XOPTS} \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --prefix %{i}
