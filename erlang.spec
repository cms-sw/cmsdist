### RPM external erlang R16B03-1
Source0: http://erlang.org/download/otp_src_%{realversion}.tar.gz
#Source1: git+https://github.com/erlang/otp.git?obj=master/OTP_R16B03-1&export=./&filter=*lib/*&output=/R16libs.tar.gz
Source1: git+https://github.com/erlang/otp.git?obj=master/OTP_R16B03-1&export=./&output=/R16libs.tar.gz
Requires: openssl zlib

# 32-bit
Provides: libc.so.6(GLIBC_PRIVATE)
# 64-bit
Provides: libc.so.6(GLIBC_PRIVATE)(64bit)

%prep
%setup -T -b 1 -n lib
%setup -D -T -b 0 -n otp_src_%{realversion}
find . -name configure | xargs perl -p -i -e 's/-no-cpp-precomp//'

%build
# Update to the next crypto library version, which supports SHA2
rm -rf lib/crypto lib/public_key
mv ../lib/{crypto,public_key} ./lib/

%ifos darwin
%define flavour --enable-darwin-64bit
%else
%define flavour --enable-m64-build --disable-m32-build
%endif

./configure CPPFLAGS=-I$ZLIB_ROOT/include LDFLAGS=-L$ZLIB_ROOT/lib \
  --prefix=%i %flavour --without-javac --enable-shared-zlib \
  --with-ssl=$OPENSSL_ROOT --enable-dynamic-ssl-lib --without-termcap
make

%install
make install

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
