### RPM external castor 2.1.9.8
# Override default realversion since they have a "-" in the realversion
%define realversion 2.1.9-8

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
Source:  http://castorold.web.cern.ch/castorold/DIST/CERN/savannah/CASTOR.pkg/%{baseVersion}-*/%{realversion}/castor-%{realversion}.tar.gz
Patch0: castor-2.1.9.8-macosx
Patch1: castor-2.1.9.8-add-ns-ldl
Patch2: castor-2.1.9.8-rtcopy-add-rfio-dependency
Patch3: castor-2.1.9.8-fix-gcc47-cxx11

# Ugly kludge : forces libshift.x.y to be in the provides (rpm only puts libshift.so.x)
# root rpm require .x.y
Provides: libshift.so.%(echo %realversion |cut -d. -f1,2)%{libsuffix}

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -n castor-%{baseVersion}
# The macosx patch is really to get things compiling one way or another. Since
# I'm not sure this actually works / does not have regressions on linux, I
# simply do not apply it on stable platforms. 
# Hopefully at some point castor people will come up with a macosx supported
# version.
case %cmsplatf in 
  osx*)
%patch0 -p2
  ;;
esac

%patch1 -p1
%patch2 -p1

# Apply C++11 / gcc 4.7.x fixes only if using a 47x architecture.
# See http://gcc.gnu.org/gcc-4.7/porting_to.html
case %cmsplatf in
  *gcc4[789]*)
%patch3 -p1
  ;;
esac

case %cmsplatf in
  *_gcc4[012345]*) ;;
  *)
    perl -pi -e "s|-Werror|-Werror -Wno-error=unused-but-set-variable|" config/Imake.tmpl
    perl -pi -e "s|--no-undefined||" config/Imake.rules
    perl -pi -e 's|^(\s+)(\$\(MAKE\) depend)|$1#$2|' Makefile.ini
  ;;
esac

# Add CMS CXXFLAGS
sed -ibak "s/\(^CXX.*=.*\)/\1 %cms_cxxflags/g" config/Imake.tmpl

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
                             MINOR_CASTOR_VERSION=%(echo %realversion | cut -d. -f3-4 | tr '-' '.' ) \
			     LDFLAGS=-ldl

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

# Strip libraries, we are not going to debug them.
%define strip_files %i/lib
