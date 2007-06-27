### RPM external castor 2.1.1-4-CMS3
# Override default realversion since they have a "-" in the realversion
%define realversion 2.1.1-4
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
Source: cvs://:pserver:anonymous@isscvs.cern.ch:/local/reps/castor?passwd=Ah<Z&tag=-r%{downloadv}&module=CASTOR2&output=/%{n}-%{v}.source.tar.gz

# Ugly kludge : forces libshift.x.y to be in the provides (rpm only puts libshift.so.x)
# root rpm require .x.y
Provides: libshift.so.%(echo %realversion |cut -d. -f1,2)%{libsuffix}

%prep
%setup -n CASTOR2 
%build
perl -p -i -e "s!__PATCHLEVEL__!%patchLevel!;s!__BASEVERSION__!\"%baseVersion\"!;s!__TIMESTAMP__!%(date +%%s)!" h/patchlevel.h

for this in BuildCupvDaemon BuildDlfDaemon BuildNameServerDaemon BuildRHCpp \
            BuildRtcpclientd BuildSchedPlugin BuildVolumeMgrDaemon UseOracle \
            UseScheduler BuildOraCpp BuildStageDaemon; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildSchedPlugin BuildJob BuildRmMaster; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildTapeDaemon; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tNO/g" config/site.def
done

for this in BuildRfioClient BuildRfioLibrary BuildStageClient BuildStageLibrary; do
    perl -pi -e "s/$this(?: |\t)+.*(YES|NO)/$this\tYES/g" config/site.def
done

mkdir -p %i/bin %i/lib %i/man/man4 %i/man/man3 %i/man/man1 %i/etc/sysconfig

find . -type f -exec touch {} \;
make -f Makefile.ini Makefiles
which makedepend >& /dev/null
[ $? -eq 0 ] && make depend

make -j7 MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1) \
         MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f2)

%install
make install MAJOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f1) \
                MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f2) \
                EXPORTLIB=/ \
                DESTDIR=%i/ \
                PREFIX= \
                CONFIGDIR=etc \
                FILMANDIR=man/man4 \
                LIBMANDIR=man/man3 \
                MANDIR=man/man1 \
                LIBDIR=lib \
                BINDIR=bin \
                LIB=lib \
                BIN=bin \
                DESTDIRCASTOR=include/shift \
                TOPINCLUDE=include 
