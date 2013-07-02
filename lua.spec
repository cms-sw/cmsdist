### RPM external lua 5.1.4
Source0: http://www.lua.org/ftp/%{n}-%{realversion}.tar.gz

Requires: readline ncurses

%define islinux %(case %{cmsos} in (slc*|fc*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%build
sed -ibak "s|^CFLAGS=|CFLAGS=-fPIC -I${READLINE_ROOT}/include -I${NCURSES_ROOT}/include|g" src/Makefile
sed -ibak "s|^LIBS=|LIBS=-L${READLINE_ROOT}/lib -L${NCURSES_ROOT}/lib|g;" src/Makefile
%if %islinux
make linux
%endif
%if %isdarwin
make macosx
%endif

%install
make install INSTALL_TOP=%{i}
%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
