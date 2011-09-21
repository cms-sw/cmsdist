### RPM external gdbm 1.8.3
Source: http://ftp.gnu.org/gnu/gdbm/gdbm-%realversion.tar.gz

%define thisuser %(id -u)
%define thisgroup %(id -g)

%prep
%setup -n %n-%{realversion}

%build
perl -p -i -e "s|BINOWN = bin|BINOWN = %{thisuser}|g" Makefile.in
perl -p -i -e "s|BINGRP = bin|BINGRP = %{thisgroup}|g" Makefile.in
./configure --prefix=%{i}
make %makeprocesses

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# Look up documentation online.
%define drop_files %i/{info,man}
