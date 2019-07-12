### RPM external dcap 2.47.12
%define tag 5753eec777a47908a40de670094903ce6b13176b
%define branch cms/%{realversion}
%define github_user cms-externals
Source: git+https://github.com/%github_user/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

BuildRequires: autotools
Requires: zlib

%prep
%setup -n %{n}-%{realversion}

%build
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
