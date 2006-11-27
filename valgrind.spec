### RPM external valgrind 3.2.1-cms1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; * ) false ;; esac
%define realversion %(echo %v | cut -d- -f1)
Source: http://www.valgrind.org/downloads/%{n}-%{realversion}.tar.bz2

%prep
%setup -n %n-%realversion
# CMS patch for segment sizes:
perl -p -i -e 's!VG_N_SEGMENTS 5000!VG_N_SEGMENTS 20000!; s!VG_N_SEGNAMES 1000!VG_N_SEGNAMES 4000!; s!VG_MAX_SEGNAMELEN 1000!VG_MAX_SEGNAMELEN 4000!' coregrind/m_aspacemgr/aspacemgr.c;

pwd

%build
./configure --prefix=%i
make %makeprocesses
%install
make install
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %i | cut -d: -f 1)
#
