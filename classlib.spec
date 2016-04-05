### RPM external classlib 3.1.3
Source: http://cmsrep.cern.ch/cmssw/cms/SOURCES/slc5_amd64_gcc472/external/classlib/3.1.3/classlib-3.1.3.tar.bz2
Patch0: classlib-3.1.3-gcc46
Patch1: classlib-3.1.3-sl6
Patch2: classlib-3.1.3-fix-gcc47-cxx11
Patch3: classlib-3.1.3-fix-unwind-x86_64
Patch4: classlib-3.1.3-memset-fix
Patch5: classlib-3.1.3-fix-obsolete-CLK_TCK

Requires: bz2lib 
Requires: pcre 
Requires: xz
Requires: openssl
Requires: zlib 

%prep
%setup -n %n-%realversion
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
# Update to get aarch64 and ppc64le
rm -f ./cfg/config.{sub,guess}
curl -L -k -s -o ./cfg/config.sub 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.sub;hb=HEAD'
curl -L -k -s -o ./cfg/config.guess 'http://git.savannah.gnu.org/gitweb/?p=config.git;a=blob_plain;f=config.guess;hb=HEAD'
chmod +x ./cfg/config.{sub,guess}

./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-openssl-includes=$OPENSSL_ROOT/include \
  --with-openssl-libraries=$OPENSSL_ROOT/lib	\
  --with-lzma-includes=$XZ_ROOT/include         \
  --with-lzma-libraries=$XZ_ROOT/lib

perl -p -i -e '
  s{-llzo2}{}g;
  !/^\S+: / && s{\S+LZO((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses CXXFLAGS="-Wno-error=extra -ansi -pedantic -W -Wall -Wno-long-long -Werror"

%install
make %makeprocesses install
