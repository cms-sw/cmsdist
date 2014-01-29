### RPM external automake 1.9.6
Source: http://ftp.gnu.org/gnu/%n/%n-%v.tar.gz
Requires: autoconf

%build
./configure --prefix=%i
make
perl -p -i -e "s|#!.*perl(.*)|#!/usr/bin/env perl$1|" aclocal automake

%post
%{relocateConfig}bin/automake-1.9
%{relocateConfig}bin/automake
%{relocateConfig}bin/aclocal-1.9
%{relocateConfig}bin/aclocal
%{relocateConfig}share/automake-1.9/Automake/Config.pm

