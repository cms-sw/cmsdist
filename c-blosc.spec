### RPM external c-blosc 1.21.6
Source: https://github.com/Blosc/c-blosc/archive/refs/tags/v%{realversion}.tar.gz
Requires: zlib zstd lz4
BuildRequires: ninja cmake

%prep
%setup -n %{n}-%{realversion}

%build
rm -rf ../build ; mkdir ../build; cd ../build
cmake ../%{n}-%{realversion} \
 -G Ninja \
 -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_INSTALL_PREFIX:STRING=%{i} \
 -DDEACTIVATE_LZ4:BOOL=OFF \
 -DDEACTIVATE_SNAPPY:BOOL=ON \
 -DDEACTIVATE_ZLIB:BOOL=OFF \
 -DDEACTIVATE_ZSTD:BOOL=OFF \
 -DDEACTIVATE_AVX2:BOOL=ON \
 -DDEACTIVATE_SSE2:BOOL=ON \
 -DPREFER_EXTERNAL_ZSTD=ON \
 -DPREFER_EXTERNAL_LZ4=ON \
 -DPREFER_EXTERNAL_ZLIB=ON \
 -DCMAKE_PREFIX_PATH="%{cmake_prefix_path}"

ninja -v %{makeprocesses}

%install
cd ../build
ninja -v %{makeprocesses} install

%post
%{relocateConfig}lib64/pkgconfig/blosc.pc
