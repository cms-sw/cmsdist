### RPM external zlib 1.1.4
Requires: gcc-wrapper
Source: http://www.gzip.org/%n/%n-%v.tar.bz2

%build
## IMPORT gcc-wrapper
case $(uname) in
  Darwin )
    LDSHARED="gcc -dynamiclib" ./configure --shared --prefix=%i
    make LIBS='libz.dylib.$(VER)' SHAREDLIB=libz.dylib # FIXME: libz.$(VER).dylib
    ;;

  * )
    ./configure --shared --prefix=%i
    make %makeprocesses
    ;;
esac

%install
case $(uname) in
  Darwin ) make install LIBS='libz.dylib.$(VER)' SHAREDLIB=libz.dylib ;;
  * ) make install ;;
esac
#
#
