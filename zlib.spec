### RPM external zlib 1.1.4
Source: http://www.gzip.org/%n/%n-%v.tar.bz2

%build
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
