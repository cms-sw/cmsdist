## INCLUDE jemalloc-common
### RPM external jemalloc %{jemalloc_version}

%build
XOPTS=""
case %{cmsplatf} in
  # set the huge page size to 16M on ARMv8
  *_aarch64_*) XOPTS="--with-lg-hugepage=24" ;;
esac

./autogen.sh ${XOPTS} \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
