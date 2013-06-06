### RPM external valgrind 3.9.0-13418
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
%define rev %(echo %{realversion} | cut -d- -f2)
Source: svn://svn.valgrind.org/valgrind/trunk?revision=%{rev}&module=%{n}-%{realversion}&output=/%{n}-%{realversion}.tar.gz
Patch1: valgrind-3.7.0-change-FN_NAME_LEN-global-buffer-size
Patch2: valgrind-3.7.0-change-VG_N_SEGMENTS-VG_N_SEGNAMES-VG_MAX_SEGNAMELEN

%prep
%setup -n %{n}-%{realversion}
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

./autogen.sh
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
