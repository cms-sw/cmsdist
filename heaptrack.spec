### RPM external heaptrack 1.4.0
Source0: https://github.com/KDE/heaptrack/archive/refs/tags/v%{realversion}.tar.gz
Source1: https://invent.kde.org/sdk/heaptrack/-/commit/c6c45f3455a652c38aefa402aece5dafa492e8ab.patch
Source2: https://github.com/KDE/heaptrack/commit/99348321819fe8efb3771b2dcd9aaffbc598b271.patch
Requires: boost libunwind zstd bz2lib zlib
BuildRequires: cmake
Provides: libc.so.6(GLIBC_PRIVATE)(64bit)
%prep
%setup -n %{n}-%{realversion}
patch -p1 <%{_sourcedir}/c6c45f3455a652c38aefa402aece5dafa492e8ab.patch
patch -p1 <%{_sourcedir}/99348321819fe8efb3771b2dcd9aaffbc598b271.patch

%build
mkdir -p %i
rm -rf ../build; mkdir ../build; cd ../build

cmake ../%{n}-%{realversion} \
   -DCMAKE_INSTALL_PREFIX=%i -DCMAKE_VERBOSE_MAKEFILE=TRUE \
   -DCMAKE_CXX_FLAGS_RELWITHDEBINFO="-g -O3" \
   -DCMAKE_PREFIX_PATH="${LIBUNWIND_ROOT};${BOOST_ROOT};${ZSTD_ROOT};${BZ2LIB_ROOT};${ZLIB_ROOT}" \
   -DHEAPTRACK_BUILD_GUI=off -DHEAPTRACK_USE_LIBUNWIND=on -DHEAPTRACK_BUILD_PRINT=on
make DEBUG=1 VERBOSE=1 %makeprocesses

%install
cd ../build
make %makeprocesses install
%define drop_files %i/share/man
