### RPM external elfutils 0.195
Source: https://sourceware.org/elfutils/ftp/%{realversion}/elfutils-%{realversion}.tar.bz2
BuildRequires: gmake bison flex
Requires: zlib bz2lib xz
%define keep_pkgconfig true

%prep
%setup -n %{n}-%{realversion}
%if "%{rhel}" == "8"
sed -i -e 's|^readelf_LDADD\s*[+]=\s*libthread.a|readelf_LDADD += libthread.a -lpthread|' src/Makefile.am
autoreconf -fi
%endif

%build
export CPPFLAGS="-I${ZLIB_ROOT}/include -I${BZ2LIB_ROOT}/include -I${XZ_ROOT}/include"
export LDFLAGS="-L${ZLIB_ROOT}/lib -L${BZ2LIB_ROOT}/lib -L${XZ_ROOT}/lib"
./configure --prefix=%{i} --disable-static --enable-install-elfh \
            --disable-libdebuginfod --disable-debuginfod \
            --enable-thread-safety --disable-nls
make %{makeprocesses} V=1

%install
make install V=1

#### FIXME: For next full rebuild fix xz to ave pkgconfig ###
#We do not have xz/lib/pkgconfig/liblzma.pc file so lets remove liblzma from Requires and explicitly link lzma
if grep ' liblzma' %i/lib/pkgconfig/libdw.pc ; then
  # Remove explicit Requires of liblzma
  sed -i -e 's| liblzma||'  %i/lib/pkgconfig/libdw.pc
  # Added our lzma include and lib paths
  sed -i -e "s|^Cflags: |Cflags: -I${XZ_ROOT}/include |" %i/lib/pkgconfig/libdw.pc
  sed -i -e "s|^Libs.private: |Libs.private: -L${XZ_ROOT}/lib -llzma |" %i/lib/pkgconfig/libdw.pc
fi

%post
%relocateConfigAll lib/pkgconfig *.pc
%{relocateConfig}bin/eu-make-debug-archive
