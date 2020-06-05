### RPM external gdb 9.2
Source: https://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

Patch0: gdb-9.2-fix-PYTHONHOME
Patch1: gdb-disable-makeinfo

Requires: python zlib xz expat

BuildRequires: autotools

%prep
%setup -n %n-%realversion
%patch0 -p1
%patch1 -p1

%build

pushd gdb
  autoreconf -fiv
popd

rm -rf ../build; mkdir ../build; cd ../build
../%n-%realversion/configure --prefix=%{i} \
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
cd ../build
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
