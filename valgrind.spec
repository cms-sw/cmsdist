### RPM external valgrind 3.6.1
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
%define realversion %(echo %v | cut -d- -f1)
Source: http://www.valgrind.org/downloads/%{n}-%{realversion}.tar.bz2
Patch1: valgrind-vg330-global
Patch2: valgrind-vg350-coregrind_n_segments

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
# CMS patch for segment sizes:
perl -p -i -e 's!VG_N_SEGMENTS 5000!VG_N_SEGMENTS 20000!; s!VG_N_SEGNAMES 1000!VG_N_SEGNAMES 4000!; s!VG_MAX_SEGNAMELEN 1000!VG_MAX_SEGNAMELEN 4000!' coregrind/m_aspacemgr/aspacemgr.c;

pwd

%build
# FIXME: This is really a hack that should be included in
# GCC spec for non system compilers.
case %cmsos in
  osx*_*_gcc421) ;;
  osx*) CFLAGS="-D__private_extern__=extern" ;;
  *) ;;
esac

./configure --prefix=%i --without-mpicc --disable-static --enable-only64bit ${CFLAGS+CFLAGS=$CFLAGS}
make %makeprocesses
%install
make install
%define strip_files %i/lib %i/bin/{cg_merge,no_op*,valgrind*}
%define drop_files %i/lib/valgrind/*.a %i/share

perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' $(grep -r -e "^#!.*perl.*" %i | cut -d: -f 1)
# I don't see how to make perl options work nicely with env, so drop the -w
# in these two scripts
perl -p -i -e 's|perl -w|perl|' %i/bin/callgrind_annotate
perl -p -i -e 's|perl -w|perl|' %i/bin/callgrind_control
