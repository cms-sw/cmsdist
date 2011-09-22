### RPM external lua 5.1.4
Source0: http://www.lua.org/ftp/lua-%realversion.tar.gz

%build
perl -p -i -e 's|^CFLAGS=|CFLAGS=-fPIC|' src/Makefile
perl -p -i -e 's|-lhistory||;s|-lncurses||' src/Makefile
case %cmsplatf in
  osx*) make macosx ;;
  *) make linux ;;
esac
%install
make install INSTALL_TOP=%i
%define keep_archives true
%define strip_files %i/{lib,bin}
%define drop_files %i/{share,man}
