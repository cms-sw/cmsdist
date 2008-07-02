### RPM lcg root 5.18.00a
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz

Patch0: root-5.18-00-libpng
Patch1: root-5.18-00a-CINT-maxlongline
Patch2: root_5.18-00-CINTFunctional
Patch3: root-5.18-00a-TBufferXML
Patch4: root-5.18-00a-Cintex
Patch5: root-5.18-00a-Cintex2
Patch6: root-5.18-00a-TBufferFile
Patch7: root-5.18-00a-cintexquickfix2
Patch8: root-5.18-00a-gendict-performance

%define cpu %(echo %cmsplatf | cut -d_ -f2)
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f1,2)

Requires: gccxml gsl castor libjpg dcap pcre python

%if "%cmsplatf" != "slc4onl_ia32_gcc346"
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
%patch2 -p0
%patch3 -p1
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p1

%build
mkdir -p %i
export ROOTSYS=%_builddir/root

%if "%cmsplatf" == "slc4onl_ia32_gcc346"
# Build without mysql, and use system qt.
# Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="
             --disable-mysql
             --disable-xrootd
             --disable-odbc
             --enable-qt"
%else
EXTRA_CONFIG_ARGS="
             --with-xrootd=$XROOTD_ROOT
             --enable-mysql --with-mysql-libdir=${MYSQL_ROOT}/lib --with-mysql-incdir=${MYSQL_ROOT}/include
             --enable-qt --with-qt-libdir=${QT_ROOT}/lib --with-qt-incdir=${QT_ROOT}/include 
             --with-ssl-incdir=${OPENSSL_ROOT}/include
             --with-ssl-libdir=${OPENSSL_ROOT}/lib"
%endif

CONFIG_ARGS="--enable-table 
             --disable-builtin-pcre
             --disable-builtin-freetype
             --disable-builtin-zlib
             --with-gccxml=${GCCXML_ROOT} 
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python2.4 
             --enable-explicitlink 
             --enable-qtgsi
             --enable-mathcore 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --enable-roofit
             --disable-ldap
             --disable-krb5
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-xml ${EXTRA_CONFIG_ARGS}"

%if (("%cmsplatf" == "slc4_ia32_gcc412")||("%cmsplatf" == "slc4_ia32_gcc422")||("%cmsplatf" == "slc4_amd64_gcc345"))
  CONFIG_ARGS="$CONFIG_ARGS --disable-cern"
%endif

case $(uname)-$(uname -p) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift --disable-astiff --disable-cern;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS --with-shift-libdir=${CASTOR_ROOT}/lib --with-shift-incdir=${CASTOR_ROOT}/include/shift;;
  Darwin*)
    ./configure macosx $CONFIG_ARGS --disable-rfio;;
  Linux-ppc64*)
    ./configure linux $CONFIG_ARGS --disable-rfio;;
esac

make  %makeprocesses
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
cp -r reflex/python/genreflex $ROOTSYS/lib/python
#

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# rootcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcore
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootcore version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Cint>
<lib name=Core>
<lib name=RIO>
<lib name=Net>
<lib name=Tree>
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

# root toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/root
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=root version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TreePlayer>
<lib name=Gpad>
<lib name=Graf3d>
<lib name=Graf>
<lib name=Hist>
<lib name=Matrix>
<lib name=Physics>
<lib name=Postscript>
<use name=ROOTCore>
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

# rootinteractive toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootinteractive
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootinteractive version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Rint>
<lib name=GQt>
<use name=qt>
<use name=libjpg>
<use name=libpng>
<use name=ROOT>
</Tool> 
EOF_TOOLFILE

# rootmath toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmath
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootmath version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=MathCore>
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
<use name=ROOT>
</Tool>
EOF_TOOLFILE

# rootminuit2 toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit2
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootminuit2 version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Minuit2>
<use name=ROOT>
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
<use name=ROOT>
</Tool> 
EOF_TOOLFILE

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootroofit
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootroofit version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=RooFitCore>
<lib name=RooFit>
<use name=ROOTMinuit>
<use name=ROOTHtml>
</Tool> 
EOF_TOOLFILE

# rootmlp toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmlp
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootmlp version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=MLP>
<use name=ROOT>
</Tool> 
EOF_TOOLFILE

# roottmva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roottmva
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=roottmva version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=TMVA>
<use name=ROOTMLP>
</Tool> 
EOF_TOOLFILE

# rootthread toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootthread
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=rootthread version=%v>
<info url="http://root.cern.ch/root/"></info>
<lib name=Thread>
<use name=ROOTCore>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/root
%{relocateConfig}etc/scram.d/rootcore
%{relocateConfig}etc/scram.d/roothistmatrix
%{relocateConfig}etc/scram.d/rootcintex
%{relocateConfig}etc/scram.d/rootinteractive
%{relocateConfig}etc/scram.d/rootmath
%{relocateConfig}etc/scram.d/rootminuit
%{relocateConfig}etc/scram.d/rootminuit2
%{relocateConfig}etc/scram.d/rootrflx
%{relocateConfig}etc/scram.d/roothtml
%{relocateConfig}etc/scram.d/rootroofit
%{relocateConfig}etc/scram.d/rootmlp
%{relocateConfig}etc/scram.d/roottmva
%{relocateConfig}etc/scram.d/rootthread
