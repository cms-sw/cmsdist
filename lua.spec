### RPM external lua 5.1.4
Source0: http://www.lua.org/ftp/%{n}-%{realversion}.tar.gz

Requires: readline ncurses

%build
sed -ibak "s|^CFLAGS=|CFLAGS=-fPIC -I${READLINE_ROOT}/include -I${NCURSES_ROOT}/include|g" src/Makefile
sed -ibak "s|^LIBS=|LIBS=-L${READLINE_ROOT}/lib -L${NCURSES_ROOT}/lib|g;" src/Makefile
%ifos linux
make linux
%endif
%ifos darwin
make macosx
%endif

%install
make install INSTALL_TOP=%{i}
%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}
