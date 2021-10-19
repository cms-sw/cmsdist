## INCLUDE jemalloc-common
### RPM external jemalloc %{jemalloc_version}

%build

./autogen.sh --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
