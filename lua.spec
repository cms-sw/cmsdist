### RPM external lua 5.1.4
Source0: http://www.lua.org/ftp/lua-%realversion.tar.gz

%build
perl -p -i -e 's|^CFLAGS=|CFLAGS=-fPIC|' src/Makefile
case %cmsplatf in
  osx*)
    make macosx
  ;;
  *)
    make linux
  ;;
esac
%install
make install INSTALL_TOP=%i
