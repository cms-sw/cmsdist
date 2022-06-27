## INCLUDE jemalloc-common
### RPM external jemalloc-debug %{jemalloc_version}

%build
./autogen.sh \
  --enable-shared \
  --disable-static \
  --disable-doc \
  --enable-stats \
  --enable-debug \
  --enable-fill \
  --prefix %{i}

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
