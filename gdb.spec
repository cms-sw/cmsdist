### RPM external gdb 7.12
Source: http://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

Patch0: gdb-7.12-fix-PYTHONHOME
Patch1: gdb-disable-makeinfo
Patch2: gdb-7.11-set-autoconf-version
# PR breakpoints/20653
# https://github.com/bminor/binutils-gdb/commit/e742d386c480efa5229bc8b1887a7718f840a457
Patch3: gdb-gcc7

Requires: python zlib xz expat

BuildRequires: autotools

%prep
%setup -n %n-%realversion
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

pushd gdb
  autoreconf -fiv
popd

./configure --prefix=%{i} \
            --disable-rpath \
            --with-system-gdbinit=%{i}/share/gdbinit \
            --with-expat=yes \
            --with-libexpat-prefix=${EXPAT_ROOT} \
            --with-zlib=yes \
            --with-python=${PYTHON_ROOT} \
            --with-lzma=yes \
            --with-liblzma-prefix=${XZ_ROOT} \
            LDFLAGS="-L${PYTHON_ROOT}/lib -L${ZLIB_ROOT}/lib -L${EXPAT_ROOT}/lib -L${XZ_ROOT}/lib" \
            CFLAGS="-Wno-error=strict-aliasing -I${PYTHON_ROOT}/include -I${ZLIB_ROOT}/include -I${EXPAT_ROOT}/include -I${XZ_ROOT}/include" \
            MAKEINFO=true
make %makeprocesses

%install
make install

cd %i/bin/
ln -s gdb gdb-%{realversion}
cat << \EOF_GDBINIT > %{i}/share/gdbinit
set substitute-path %{installroot} %{cmsroot}
EOF_GDBINIT

# To save space, clean up some things that we don't really need 
%define drop_files %i/lib %i/bin/{gdbserver,gdbtui} %i/share/{man,info,locale}

%post
%{relocateConfig}/share/gdbinit
