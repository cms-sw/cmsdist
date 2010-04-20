### RPM external castor 2.1.9.4
# Override default realversion since they have a "-" in the realversion
%define realversion %(echo %v | sed 's|\\.\\([^\\.]\\{1,\\}\\)$|-\\1|')

## BUILDIF case $(uname):$(uname -p) in Linux:i*86 ) true ;; Linux:x86_64 ) true ;;  Linux:ppc64 ) false ;; Darwin:* ) false ;; * ) true ;; esac
%define downloadv v%(echo %realversion | tr - _ | tr . _)
%define baseVersion %(echo %realversion | cut -d- -f1)
%define patchLevel %(echo %realversion | cut -d- -f2)
%define cpu %(echo %cmsplatf | cut -d_ -f2)
%if "%cpu" != "amd64"
%define libsuffix %nil
%else
%define libsuffix ()(64bit)
%endif

#Source: http://cern.ch/castor/DIST/CERN/savannah/CASTOR.pkg/%realversion/castor-%downloadv.tar.gz
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{v}.source.tar.gz
#Source: cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/castor?passwd=Ah<Z&tag=-r%{downloadv}&module=CASTOR2&output=/%{n}-%{realversion}.source.tar.gz
Source:  http://castor.web.cern.ch/castor/DIST/CERN/savannah/CASTOR.pkg/%{baseVersion}-*/%{realversion}/castor-%{realversion}.tar.gz
Patch0: castor-2.1.9.4-gcc43
Patch1: castor-2.1.9.4-gcc44

# Ugly kludge : forces libshift.x.y to be in the provides (rpm only puts libshift.so.x)
# root rpm require .x.y
Provides: libshift.so.%(echo %realversion |cut -d. -f1,2)%{libsuffix}

%prep
%setup -n castor-%{baseVersion}

%patch0 -p1
%patch1 -p1

%build

# make sure the version gets properly set up as otherwise it's "unknown" to the server
# to check: " %i/bin/castor -v " should give back the version
perl -pi -e "s/\ \ __MAJORVERSION__/%(echo %realversion | cut -d. -f1)/" h/patchlevel.h
perl -pi -e "s/\ \ __MINORVERSION__/%(echo %realversion | cut -d. -f2)/" h/patchlevel.h
perl -pi -e "s/\ \ __MAJORRELEASE__/%(echo %realversion | cut -d. -f3 | cut -d- -f 1 )/" h/patchlevel.h
perl -pi -e "s/\ \ __MINORRELEASE__/%(echo %realversion | cut -d- -f2)/" h/patchlevel.h

perl -p -i -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h

mkdir -p %i/bin %i/lib %i/etc/sysconfig

find . -type f -exec touch {} \;

CASTOR_NOSTK=yes; export CASTOR_NOSTK

make -f Makefile.ini Makefiles
which makedepend >& /dev/null
[ $? -eq 0 ] && make depend
make %{makeprocesses} client MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1-2) \
                             MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' )

%install
make installclient \
                MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1-2) \
                MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' ) \
                EXPORTLIB=/ \
                DESTDIR=%i/ \
                PREFIX= \
                CONFIGDIR=etc \
                FILMANDIR=usr/share/man/man4 \
                LIBMANDIR=usr/share/man/man3 \
                MANDIR=usr/share/man/man1 \
                LIBDIR=lib \
                BINDIR=bin \
                LIB=lib \
                BIN=bin \
                DESTDIRCASTOR=include/shift \
                TOPINCLUDE=include 

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <lib name="shift"/>
    <client>
      <environment name="CASTOR_BASE" default="%i"/>
      <environment name="INCLUDE" default="$CASTOR_BASE/include"/>
      <environment name="LIBDIR" default="$CASTOR_BASE/lib"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
