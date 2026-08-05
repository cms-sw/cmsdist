## INCLUDE rocm-config
### RPM external rocgdb %{rocm_version_num}

Source0: https://github.com/ROCm/ROCgdb/archive/refs/tags/therock-%{rocm_version_num}.tar.gz
Requires: xz zstd zlib python3 expat
Requires: rocdbgapi rocm-comgr rocr-runtime
BuildRequires: python3 expat zlib xz
BuildRequires: bison flex

%prep
%setup -q -n ROCgdb-therock-%{rocm_version_num}

%build
mkdir -p build
cd build
export PKG_CONFIG_PATH=$ROCDBGAPI_ROOT/share/pkgconfig:$PKG_CONFIG_PATH
../configure \
    --prefix=%{i} \
    --program-prefix=roc \
    --enable-64-bit-bfd \
    --enable-targets="%{_arch}-linux-gnu,amdgcn-amd-amdhsa" \
    --disable-ld --disable-gas --disable-gdbserver --disable-sim \
    --disable-binutils --disable-gprof \
    --enable-tui --disable-gdbtk --disable-gprofng --disable-shared \
    --with-expat --with-libexpat-prefix=$EXPAT_ROOT \
    --with-lzma --with-liblzma-prefix=$XZ_ROOT \
    --with-system-zlib --without-guile \
    --without-babeltrace \
    --with-python=python3 \
    CPPFLAGS="-I$EXPAT_ROOT/include -I$XZ_ROOT/include -I$ZLIB_ROOT/include" \
    LDFLAGS="-L$EXPAT_ROOT/lib -L$XZ_ROOT/lib -L$ZLIB_ROOT/lib -L$PYTHON3_ROOT/lib"

make %{makeprocesses}

%install
cd build
make install
