### RPM external gdb 10.2
Source: https://ftp.gnu.org/gnu/%{n}/%{n}-%{realversion}.tar.gz

Patch0: gdb-disable-makeinfo

Requires: python3 zlib xz expat py3-six

%prep
%setup -n %n-%realversion
%patch0 -p1

%build
rm -rf ../build; mkdir ../build; cd ../build
../%n-%realversion/configure --prefix=%{i} \
            --disable-rpath \
            --with-system-gdbinit=%{i}/share/gdbinit \
            --with-expat=yes \
            --with-libexpat-prefix=${EXPAT_ROOT} \
            --with-zlib=yes \
            --with-python=$(which python3) \
            --with-lzma=yes \
            --with-liblzma-prefix=${XZ_ROOT} \
            LDFLAGS="-L${PYTHON3_ROOT}/lib -L${ZLIB_ROOT}/lib -L${EXPAT_ROOT}/lib -L${XZ_ROOT}/lib" \
            CFLAGS="-Wno-error=strict-aliasing -I${PYTHON3_ROOT}/include -I${ZLIB_ROOT}/include -I${EXPAT_ROOT}/include -I${XZ_ROOT}/include" \
            MAKEINFO=true
make %makeprocesses

%install
cd ../build
make install

cd %i/bin/
mv gdb gdb-%{realversion}
cat << \EOF_GDBINIT > %{i}/share/gdbinit
set substitute-path %{installroot} %{cmsroot}
EOF_GDBINIT

echo "#!/bin/bash" > gdb
echo "PYTHONHOME=${PYTHON3_ROOT} gdb-%{realversion} \"\$@\"" >> gdb
chmod +x gdb

# To save space, clean up some things that we don't really need 
%define drop_files %i/lib %i/bin/{gdbserver,gdbtui} %i/share/{man,info,locale}

%post
%{relocateConfig}/share/gdbinit
%{relocateConfig}/bin/gdb
