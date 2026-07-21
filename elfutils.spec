### RPM external elfutils 0.195
Source: https://sourceware.org/elfutils/ftp/%{realversion}/elfutils-%{realversion}.tar.bz2
BuildRequires: gmake bison flex
Requires: zlib bz2lib xz
%define keep_pkgconfig true

%prep
%setup -n %{n}-%{realversion}

%build
export CPPFLAGS="-I${ZLIB_ROOT}/include -I${BZ2LIB_ROOT}/include -I${XZ_ROOT}/include"
export LDFLAGS="-L${ZLIB_ROOT}/lib -L${BZ2LIB_ROOT}/lib -L${XZ_ROOT}/lib"
./configure --prefix=%{i} --disable-static --enable-install-elfh \
            --disable-libdebuginfod --disable-debuginfod \
            --enable-thread-safety --disable-nls
make %{makeprocesses}

%install
make install

%post
%relocateConfigAll lib/pkgconfig *.pc
