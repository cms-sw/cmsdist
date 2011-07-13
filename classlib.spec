### RPM external classlib 3.1.2
Source: http://cmsmac01.cern.ch/~lat/exports/%n-%realversion.tar.bz2
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)
Patch0: classlib-3.1.2-gcc46

Requires: bz2lib 
Requires: pcre 
%if "%online" != "true"
Requires: openssl
Requires: zlib 
%else
Requires: onlinesystemtools
%endif

%prep
%setup -n %n-%realversion
case %gccver in
  4.6.*)
%patch0 -p1
  ;;
esac

%build
./configure --prefix=%i                         \
  --with-zlib-includes=$ZLIB_ROOT/include       \
  --with-zlib-libraries=$ZLIB_ROOT/lib          \
  --with-bz2lib-includes=$BZ2LIB_ROOT/include   \
  --with-bz2lib-libraries=$BZ2LIB_ROOT/lib      \
  --with-pcre-includes=$PCRE_ROOT/include       \
  --with-pcre-libraries=$PCRE_ROOT/lib          \
  --with-openssl-includes=$OPENSSL_ROOT/include \
  --with-openssl-libraries=$OPENSSL_ROOT/lib

perl -p -i -e '
  s{-l(lzo2|lzma)}{}g;
  !/^\S+: / && s{\S+LZ(O|MA)((C|Dec)ompressor|Constants|Error)\S+}{}g' \
 Makefile

make %makeprocesses

%install
make %makeprocesses install
