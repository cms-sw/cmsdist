### RPM lcg root 5.22.00d
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i 
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Patch0:  root-5.18-00-libpng 
Patch1:  root-5.21-04-CINT-maxlongline
Patch2:  root-5.22-00-TMVA-shut-the-hell-up-for-once
Patch3:  root-5.22-00a-TMVA-shut-the-hell-up-again
Patch4:  root-5.22-00d-fireworks-graf3d-gui
Patch5:  root-5.22-00a-roofit-silence-static-printout
Patch6: root-5.22-00a-TMVA-just-shut-the-hell-up
Patch7: root-5.22-00a-th1
Patch8: root-5.22-00a-smatrix
Patch9: root-5.22-00a-fireworks1
Patch10: root-5.22-00a-gcc44
Patch11: root-5.22-00a-fireworks2
Patch12: root-5.22-00a-fireworks3
Patch13: root-5.22-00a-gcc43-array-bounds-dictionary-workaround
Patch14: root-5.22-00a-fireworks4
Patch15: root-5.22-00d-fireworks5

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f1,2)

Requires: gccxml gsl castor libjpg dcap pcre python

%if "%online" != "true"
Requires: qt openssl mysql libpng zlib libungif xrootd
%else
%define skiplibtiff true
%endif

%if "%cpu" == "amd64"
%define skiplibtiff true
%endif

%if "%skiplibtiff" != "true"
Requires: libtiff
%endif

%prep
%setup -n root
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# patch10 is compiler version dependent, see below
%patch11 -p1
%patch12 -p1
# patch13 is compiler version dependent, see below

# work around patch issue...
rm graf3d/gl/src/gl2ps.c
%patch14 -p1
#work around patch issues in patch14(?)
rm graf3d/eve/inc/TEveLegoOverlay.h.orig
rm graf3d/eve/src/TEveLegoOverlay.cxx
rm graf3d/gl/inc/gl2ps.h.orig
rm graf3d/gl/src/gl2ps.c.orig
%patch15 -p1

case %gccver in
  4.3.*)
%patch13 -p1
  ;;
  4.4.*)
%patch10 -p1
  ;;
esac
 
%build

mkdir -p %i
export ROOTSYS=%_builddir/root

%if "%online" == "true"
# Build without mysql, and use system qt.
# Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="--with-f77=/usr
             --disable-mysql
             --disable-xrootd
             --disable-odbc
             --disable-qt --disable-qtgsi"
%else
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}
             --with-xrootd=$XROOTD_ROOT
             --enable-mysql --with-mysql-libdir=${MYSQL_ROOT}/lib --with-mysql-incdir=${MYSQL_ROOT}/include
             --enable-qt --with-qt-libdir=${QT_ROOT}/lib --with-qt-incdir=${QT_ROOT}/include 
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib
	     --enable-qtgsi"
%endif

CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python2.4 
             --enable-explicitlink 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --disable-ldap
             --disable-krb5
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-xml ${EXTRA_CONFIG_ARGS}"

#case %gccver in
#  4.*)
#  CONFIG_ARGS="$CONFIG_ARGS --disable-cern"
#  ;;
#esac

case $(uname)-$(uname -p) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift --disable-astiff;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift;;
  Darwin*)
    ./configure macosx $CONFIG_ARGS --disable-rfio --disable-builtin_afterimage ;;
  Linux-ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

case %cmsplatf in
  osx*)
   makeopts=
  ;;
  *)
   makeopts="%makeprocesses"
  ;;
esac
 
make $makeopts 
make cintdlls

%install
# Override installers if we are using GNU fileutils cp.  On OS X
# ROOT's INSTALL is defined to "cp -pPR", which only works with
# the system cp (/bin/cp).  If you have fileutils on fink, you
# lose.  Check which one is getting picked up and select syntax
# accordingly.  (FIXME: do we need to check that -P is accepted?)
if (cp --help | grep -e '-P.*--parents') >/dev/null 2>&1; then
  cp="cp -dpR"
else
  cp="cp -pPR"
fi

export ROOTSYS=%i
make INSTALL="$cp" INSTALLDATA="$cp" install
mkdir -p $ROOTSYS/lib/python
cp -r cint/reflex/python/genreflex $ROOTSYS/lib/python
#

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# rootcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcore
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootcore version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Tree>
<lib name=Net>
<lib name=Thread>
<lib name=MathCore>
<lib name=RIO>
<lib name=Core>
<lib name=Cint>
<Client>
 <Environment name=ROOTCORE_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$ROOTCORE_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$ROOTCORE_BASE/include"></Environment>
 <Environment name=INCLUDE default="$ROOTCORE_BASE/cint"></Environment>
</Client>
<use name=sockets>
<use name=pcre>
<use name=zlib>
<Runtime name=PATH value="$ROOTCORE_BASE/bin" type=path>
<Runtime name=ROOTSYS value="$ROOTCORE_BASE/">
<Runtime name=PYTHONPATH value="$ROOTCORE_BASE/lib" type=path>
</Tool>
EOF_TOOLFILE

# root toolfile, alias for rootphysics. Using rootphysics is preferred.
cat << \EOF_TOOLFILE >%i/etc/scram.d/root
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=root version=%v>
<info url="http://root.cern.ch/root/"></info>
<use name=rootphysics>
</Tool>
EOF_TOOLFILE

# roothistmatrix toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothistmatrix
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roothistmatrix version=%v> 
<info url="http://root.cern.ch/root/"></info>
<lib name=Hist>
<lib name=Matrix>
<use name=ROOTCore>
</Tool>
EOF_TOOLFILE

# rootgpad toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgpad
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootgpad version=%v> 
<info url="http://root.cern.ch/root/"></info>
<lib name=Gpad>
<lib name=Graf>
<use name=roothistmatrix>
</Tool>
EOF_TOOLFILE

# rootphysics toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootphysics
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootphysics version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Physics>
<use name=roothistmatrix>
</Tool>
EOF_TOOLFILE

# rootgraphics toolfile, identical to old "root" toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgraphics
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootgraphics version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TreePlayer>
<lib name=Graf3d>
<lib name=Postscript>
<use name=rootgpad>
</Tool>
EOF_TOOLFILE

# rootcintex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcintex
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootcintex version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Cintex>
<use name=ROOTRflx>
<use name=ROOTCore>
</Tool>
EOF_TOOLFILE

# (temporarily eviscerated) rootinteractive toolfile (GQt/qt lib dependencies
# have been removed for the moment)
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootinteractive
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootinteractive version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Rint>
<lib name=GQt>
<lib name=Gui>
<use name=qt>
<use name=libjpg>
<use name=libpng>
<use name=rootgpad>
</Tool> 
EOF_TOOLFILE

# rootmath toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmath
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootmath version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=GenVector>
<lib name=MathMore>
<use name=ROOTCore>
<use name=gsl>
</Tool>
EOF_TOOLFILE

# rootminuit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootminuit version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Minuit>
<use name=rootgpad>
</Tool>
EOF_TOOLFILE

# rootminuit2 toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit2
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootminuit2 version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Minuit2>
<use name=rootgpad>
</Tool>
EOF_TOOLFILE

# rootrflx toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrflx
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootrflx version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Reflex>
<Client>
 <Environment name=ROOTRFLX_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$ROOTRFLX_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$ROOTRFLX_BASE/include"></Environment>
</Client>
<use name=sockets>
<use name=gccxml>
<Runtime name=PATH value="$ROOTRFLX_BASE/bin" type=path>
<Runtime name=ROOTSYS value="$ROOTRFLX_BASE/">
<Runtime name=GENREFLEX value="$ROOTRFLX_BASE/bin/genreflex">
</Tool>
EOF_TOOLFILE

# roothtml toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothtml
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roothtml version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Html>
<use name=rootgpad>
</Tool> 
EOF_TOOLFILE

# rootmlp toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmlp
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootmlp version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=MLP>
<use name=RootGraphics>
</Tool> 
EOF_TOOLFILE

# roottmva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roottmva
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roottmva version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TMVA>
<use name=ROOTMLP>
<use name=rootminuit>
</Tool> 
EOF_TOOLFILE

# rootthread toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootthread
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootthread version=%v>
<info url="http://root.cern.ch/root/"></info>
<use name=ROOTCore>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/root
%{relocateConfig}etc/scram.d/rootcore
%{relocateConfig}etc/scram.d/roothistmatrix
%{relocateConfig}etc/scram.d/rootphysics
%{relocateConfig}etc/scram.d/rootgraphics
%{relocateConfig}etc/scram.d/rootcintex
%{relocateConfig}etc/scram.d/rootinteractive
%{relocateConfig}etc/scram.d/rootmath
%{relocateConfig}etc/scram.d/rootminuit
%{relocateConfig}etc/scram.d/rootminuit2
%{relocateConfig}etc/scram.d/rootrflx
%{relocateConfig}etc/scram.d/roothtml
%{relocateConfig}etc/scram.d/rootmlp
%{relocateConfig}etc/scram.d/roottmva
%{relocateConfig}etc/scram.d/rootthread
