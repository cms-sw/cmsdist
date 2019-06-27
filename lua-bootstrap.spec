### RPM external lua-bootstrap 5.2.4
Source0: http://www.lua.org/ftp/lua-%{realversion}.tar.gz

%define keep_archives true
%define strip_files %{i}/{lib,bin}
%define drop_files %{i}/{share,man}

%prep  
%setup -n lua-%{realversion}

%build
make -C src all MYLIBS="-ldl" MYCFLAGS="-fPIC -DLUA_USE_POSIX -DLUA_USE_DLOPEN"

%install
make install INSTALL_TOP=%{i}
# bla bla
