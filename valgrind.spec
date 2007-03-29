### RPM external valgrind 3.2.3-cms1
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) true ;; * ) false ;; esac
%define realversion %(echo %v | cut -d- -f1)
Source: http://www.valgrind.org/downloads/%{n}-%{realversion}.tar.bz2
Patch1: valgrind-vg323-p2-global
Patch2: valgrind-vg323-p2-dump

%prep
%setup -n %n-%realversion
%patch1 -p0
%patch2 -p0
# CMS patch for segment sizes:
perl -p -i -e 's!VG_N_SEGMENTS 5000!VG_N_SEGMENTS 20000!; s!VG_N_SEGNAMES 1000!VG_N_SEGNAMES 4000!; s!VG_MAX_SEGNAMELEN 1000!VG_MAX_SEGNAMELEN 4000!' coregrind/m_aspacemgr/aspacemgr.c;

pwd

%build
./configure --prefix=%i
make %makeprocesses
%install
make install
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %i | cut -d: -f 1)
# I don't see how to make perl options work nicely with env, so drop the -w
# in these two scripts
perl -p -i -e 's|perl -w|perl|' %i/bin/callgrind_annotate
perl -p -i -e 's|perl -w|perl|' %i/bin/callgrind_control
