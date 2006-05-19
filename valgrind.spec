### RPM external valgrind 3.1.1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; * ) false ;; esac
Source: http://www.valgrind.org/downloads/%{n}-%{v}.tar.bz2
%build
./configure --prefix=%i
make %makeprocesses
%install
make install
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %i | cut -d: -f 1)
