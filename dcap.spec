### RPM external dcap 2.47.8
Source0: git://github.com/dCache/dcap.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: dcap-2.47.5.0-macosx
Patch1: dcap-2.47.5.0-fork-safety

BuildRequires: autotools
Requires: zlib

%prep
%setup -n %{n}-%{realversion}
# THIS PATCH IS COMPLETELY UNTESTED AND HAS THE SOLE PURPOSE OF BUILDING STUFF
# ON MAC, REGARDLESS WHETHER IT WORKS OR NOT. It is however safe to include,
# since every change is ifdeffed with __APPLE__.
%patch0 -p1
# Apply fork safety patch from Brian Bockelman
%patch1 -p0

%build
unset MAGIC

# Since we are using the checked out code, we need to regenerate the auto-tools
# crap.
# There is also a problem with the way they define library_includedir which I could fix only like this.
perl -p -i -e 's|library_includedir.*|library_includedir\=\$(includedir)|' src/Makefile.am
mkdir -p config
aclocal -I config
autoheader
libtoolize --automake
automake --add-missing --copy --foreign
autoconf 
./configure --prefix %{i} CFLAGS="-I${ZLIB_ROOT}/include" LDFLAGS="-L${ZLIB_ROOT}/lib"

# We don't care about the plugins and other stuff and build only the source.
make -C src %makeprocesses
%install
make -C src install

# Strip libraries, we are not going to debug them.
%define strip_files %{i}/lib
# Look up documentation online.
%define drop_files %{i}/share
