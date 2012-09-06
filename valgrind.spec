### RPM external valgrind 3.8.0
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
%define realversion %(echo %v | cut -d- -f1)
Source: http://www.valgrind.org/downloads/%{n}-%{realversion}.tar.bz2
Patch1: valgrind-3.7.0-change-FN_NAME_LEN-global-buffer-size
Patch2: valgrind-3.7.0-change-VG_N_SEGMENTS-VG_N_SEGNAMES-VG_MAX_SEGNAMELEN

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1

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
