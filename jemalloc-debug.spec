## INCLUDE jemalloc-common
### RPM external jemalloc-debug %{jemalloc_version}

%build
# Disable documentation (not needed)
sed -ibak 's/install: install_bin install_include install_lib install_doc/install: install_bin install_include install_lib/' Makefile.in
./autogen.sh

./configure \
  --enable-stats \
  --prefix %{i} \
  --enable-debug \
  --enable-fill

%post
%{relocateConfig}bin/jemalloc.sh
%{relocateConfig}bin/jemalloc-config
