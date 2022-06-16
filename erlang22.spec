### RPM external erlang22 22.3.4.19
Source: https://github.com/erlang/otp/archive/OTP-%{realversion}.tar.gz
Requires: zlib

# Do not format man-pages and do not install miscellaneous
Patch0: erlang22_nomiscellaneous_noformat
# Remove rpath
Patch1: erlang22_remove_rpath
# Do not install C sources
Patch2: erlang22_donotinstall_C_sources
# Do not install erlang sources
Patch3: erlang22_donotinstall_Erlang_sources

# 32-bit
Provides: libc.so.6(GLIBC_PRIVATE)
# 64-bit
Provides: libc.so.6(GLIBC_PRIVATE)(64bit)

%prep
%setup -q -n otp-OTP-%{realversion}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1 -F2

%build
# Update to the next crypto library version, which supports SHA2
#rm -rf lib/crypto lib/public_key
#mv ../lib/{crypto,public_key} ./lib/

%ifos darwin
%define flavour --enable-darwin-64bit
%else
%define flavour --enable-m64-build --disable-m32-build
%endif

./configure CFLAGS="-DOPENSSL_NO_EC=1" CPPFLAGS=-I$ZLIB_ROOT/include LDFLAGS=-L$ZLIB_ROOT/lib \
  --prefix=%i %flavour --without-javac --enable-shared-zlib \
  --with-ssl --enable-dynamic-ssl-lib --without-termcap

# remove pre-built stuff
make clean

make

%install
make install

# Do not install info files - they are almost empty and useless
find %{i}/lib/erlang -type f -name info -exec rm -f {} \;

# fix 0775 permission on some directories
chmod 0755 %{i}/lib/erlang/bin

# remove empty directory
rm -r %{i}/lib/erlang/erts-*/man

# remove outdated script
rm -f %{i}/lib/erlang/Install

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$?$root = X1 || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh
%{relocateConfig}lib/erlang/bin/{erl,start}
%{relocateConfig}lib/erlang/erts-*/bin/{erl,start}
