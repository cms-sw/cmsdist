### RPM external gdbm 1.8.3
Requires: gcc-wrapper
Source: http://rm.mirror.garr.it/mirrors/gnuftp/gnu/%{n}/%{n}-%{v}.tar.gz

%define thisuser %(id -u)
%define thisgroup %(id -g)

%build
## IMPORT gcc-wrapper
perl -p -i -e "s|BINOWN = bin|BINOWN = %{thisuser}|g" Makefile.in
perl -p -i -e "s|BINGRP = bin|BINGRP = %{thisgroup}|g" Makefile.in
./configure --prefix=%{i}
make %makeprocesses
#
