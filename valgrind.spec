### RPM external valgrind 3.3.0-CMS18a
## BUILDIF case $(uname):$(uname -m) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) true ;; * ) false ;; esac
## INITENV SET VALGRIND_LIB %{i}/lib/valgrind
%define realversion %(echo %v | cut -d- -f1)
Source: http://www.valgrind.org/downloads/%{n}-%{realversion}.tar.bz2
# These two patches (originally from version 3.2.3) should still work in 3.3.0
Patch1: valgrind-vg330-global
Patch2: valgrind-vg330-dump
Patch3: valgrind-vg330-coregrind_n_segments

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
%patch3 -p1
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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<Tool name=valgrind version=%v>
<Client>
 <Environment name=VALGRIND_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$VALGRIND_BASE/include"></Environment>
</Client>
<Runtime name=PATH value="$VALGRIND_BASE/bin" type=path>
<Runtime name=VALGRIND_LIB value="$VALGRIND_BASE/lib/valgrind">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
