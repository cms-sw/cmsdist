### RPM external castor 2.1.13.9
# Override default realversion since they have a "-" in the realversion
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)

%define realversion 2.1.13-6
%define downloadv v%(echo %realversion | tr - _ | tr . _)
%define baseVersion %(echo %realversion | cut -d- -f1)
%define patchLevel %(echo %realversion | cut -d- -f2)

%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)

%if %isamd64
%define libsuffix ()(64bit)
%else
%define libsuffix %nil
%endif

Source:  http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/%{baseVersion}-*/%{realversion}/castor-%{realversion}.tar.gz

Patch0: castor-2.1.13.6-fix-pthreads-darwin
Patch1: castor-2.1.13.6-fix-memset-in-showqueues
Patch2: castor-2.1.13.9-fix-arm-m32-option
Patch3: castor-2.1.13.9-fix-arm-type-limits
Patch4: castor-2.1.13.9-fix-link-libuuid

Requires: libuuid

# Ugly kludge : forces libshift.x.y to be in the provides (rpm only puts libshift.so.x)
# root rpm require .x.y
Provides: libshift.so.%(echo %realversion |cut -d. -f1,2)%{libsuffix}

%prep
%setup -n castor-%{baseVersion}
%if %isdarwin
%patch0 -p1
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

perl -pi -e "s|-Werror|-Werror -Wno-error=unused-but-set-variable|" config/Imake.tmpl
perl -pi -e "s|--no-undefined||" config/Imake.rules

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
./configure
LDFLAGS="-L${LIBUUID_ROOT}/lib64" CXXFLAGS="-I${LIBUUID_ROOT}/include" make %{makeprocesses} client
%install
make installclient \
                MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1-2) \
                MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' ) \
                EXPORTLIB=/ \
                DESTDIR=%i \
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

rm -rf %i/bin
mv %i/usr/bin %i/bin

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
# bla bla
