### RPM external lua 5.1.5
Source0: http://www.lua.org/ftp/%{n}-%{realversion}.tar.gz

%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%build
%if %islinux
# Do not use LUA_USE_LINUX as it brings LUA_USE_READLINE
# LUA_USE_DLOPEN requires -ldl
make -C src all MYLIBS="-ldl" MYCFLAGS="-fPIC -DLUA_USE_POSIX -DLUA_USE_DLOPEN"
%endif
%if %isdawrin
# LUA_USE_MACOSX does not bring LUA_USE_READLINE, only LUA_USE_POSIX and LUA_DL_DYLD
make -C src all MYCFLAGS="-fPIC -DLUA_USE_MACOSX"
%endif

%install
make install INSTALL_TOP=%{i}
