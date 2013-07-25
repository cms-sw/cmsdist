### RPM external lua 5.1.5
Source0: http://www.lua.org/ftp/%{n}-%{realversion}.tar.gz

%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}

%build
make -C src all MYLIBS="-ldl" MYCFLAGS="-fPIC -DLUA_USE_POSIX -DLUA_USE_DLOPEN"

%install
make install INSTALL_TOP=%{i}
