### RPM external lua 5.1.4
Source0: http://www.lua.org/ftp/lua-%realversion.tar.gz

%build
# No LUA_USE_READLINE; -ldl is harmless on OS X (= -lSystem).
make -C src all MYLIBS="-ldl" MYCFLAGS="-fPIC -DLUA_USE_POSIX -DLUA_USE_DLOPEN"

%install
make install INSTALL_TOP=%i
%define keep_archives true
%define strip_files %i/{lib,bin}
%define drop_files %i/{share,man}
