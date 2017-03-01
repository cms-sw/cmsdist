### RPM external blackhat 0.9.9
Source: http://www.hepforge.org/archive/blackhat/blackhat-%{realversion}.tar.gz

Patch0: blackhat-gcc48
Patch1: blackhat-0.9.9-armv7hl
Patch2: blackhat-no_warnings
Patch3: blackhat-0.9.9-default-arg-at-first-decl

Requires: qd python openssl
%prep
%setup -n blackhat-%{realversion}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

# Update to detect aarch64 and ppc64le
rm -f ./config.{sub,guess}
curl -L -k -s -o ./config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./config.{sub,guess}

./configure --prefix=%i --with-QDpath=$QD_ROOT CXXFLAGS="-Wno-deprecated -I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib"
# The following hack insures that the bins with the library linked explicitly
# rather than indirectly, as required by the gold linker
%build
make %{makeprocesses}
%install
make install

%post
%{relocateConfig}lib/blackhat/lib*.la
%{relocateConfig}bin/blackhat-config
%{relocateConfig}bin/dataInstall
