### RPM external curl 7.20.0
Source: http://curl.haxx.se/download/%n-%realversion.tar.gz
Provides: libcurl.so.3()(64bit) 
Requires: openssl
Requires: zlib
   
%prep
%setup -n %n-%{realversion}

%build
export OPENSSL_ROOT
export ZLIB_ROOT
./configure --prefix=%i --without-libidn --disable-ldap --with-ssl=${OPENSSL_ROOT} --with-zlib=${ZLIB_ROOT}
# This should change link from "-lz" to "-lrt -lz", needed by gold linker
# This is a fairly ugly way to do it, however.
perl -p -i -e "s!\(LIBS\)!(LIBCURL_LIBS)!" src/Makefile
make %makeprocesses

%install
make install
case %cmsos in 
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac

ln -s libcurl.$SONAME %i/lib/libcurl.$SONAME.3
# Trick to get our version of curl pick up our version of its associated shared
# library (which is different from the one coming from the system!).
case %cmsos in
  osx*)
install_name_tool -id %i/lib/libcurl-cms.dylib -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib  %i/lib/libcurl.4.dylib
install_name_tool -change %i/lib/libcurl.4.dylib %i/lib/libcurl-cms.dylib %i/bin/curl
ln -s libcurl.4.dylib %i/lib/libcurl-cms.dylib
  ;;
esac

# We remove pkg-config files for two reasons:
# * it's actually not required (macosx does not even have it).
# * rpm 4.8 adds a dependency on the system /usr/bin/pkg-config 
#   on linux.
# In the case at some point we build a package that can be build
# only via pkg-config we have to think on how to ship our own
# version.
rm -rf %i/lib/pkgconfig

%post
%{relocateConfig}bin/curl-config
