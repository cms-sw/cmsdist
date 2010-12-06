### RPM lcg root 5.27.06b
## INITENV +PATH PYTHONPATH %i/lib/python
## INITENV SET ROOTSYS %i  
#Source: cvs://:pserver:cvs@root.cern.ch:2401/user/cvs?passwd=Ah<Z&tag=-rv%(echo %realversion | tr . -)&module=root&output=/%{n}_v%{realversion}.source.tar.gz
Source: ftp://root.cern.ch/%n/%{n}_v%{realversion}.source.tar.gz
%define closingbrace )
%define online %(case %cmsplatf in *onl_*_*%closingbrace echo true;; *%closingbrace echo false;; esac)

Patch0: root-5.27-06-externals
Patch1: root-5.27-04-CINT-maxlongline-maxtypedef
Patch2: root-5.22-00a-roofit-silence-static-printout
Patch3: root-5.22-00d-linker-gnu-hash-style
Patch4: root-5.22-00d-TBranchElement-dropped-data-member
Patch5: root-5.27-06-fireworks9
Patch6: root-5.27-06b-gdb-backtrace
Patch7: root-5.27-06-tmva-DecisionTreeNode
Patch8: root-5.27-06b-r36567
Patch9: root-5.27-06b-r36572
Patch10: root-5.27-06b-r36707
Patch11: root-5.27-06b-r36594
Patch12: root-5.27-06b-tmva-MethodBase-initvar
Patch13: root-5.27-06b-tmva_Event_dynamic_hack

%define cpu %(echo %cmsplatf | cut -d_ -f2)

Requires: xrootd gccxml gsl castor libjpg dcap pcre python fftw3
%if "%online" != "true"
Requires: qt openssl libpng zlib libungif libtiff
%endif

%prep
%setup -n root
%patch0 -p1
%patch1 -p1
%patch2 -p1
# patch3 is OS version dependent, see below
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1

# The following patch can only be applied on SLC5 or later (extra linker
# options only available with the SLC5 binutils)
case %cmsplatf in
  slc5_* | slc5onl_* )
%patch3 -p1
  ;;
esac

%build

mkdir -p %i
export LIBJPG_ROOT
export ROOTSYS=%_builddir/root
export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

%if "%online" == "true"
# Use system qt. Also skip xrootd and odbc for online case:

EXTRA_CONFIG_ARGS="--with-f77=/usr
             --disable-odbc
             --disable-qt --disable-qtgsi --disable-astiff"
%else
export LIBPNG_ROOT ZLIB_ROOT LIBTIFF_ROOT LIBUNGIF_ROOT
EXTRA_CONFIG_ARGS="--with-f77=${GCC_ROOT}
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
             --enable-python --with-python-libdir=${PYTHON_ROOT}/lib --with-python-incdir=${PYTHON_ROOT}/include/python${PYTHONV}
             --enable-explicitlink 
             --enable-mathmore
             --enable-reflex  
             --enable-cintex 
             --enable-minuit2 
             --enable-fftw3
             --with-fftw3-incdir=${FFTW3_ROOT}/include
             --with-fftw3-libdir=${FFTW3_ROOT}/lib
             --disable-ldap
             --disable-krb5
             --with-xrootd=${XROOTD_ROOT}
             --with-gsl-incdir=${GSL_ROOT}/include
             --with-gsl-libdir=${GSL_ROOT}/lib
             --with-dcap-libdir=${DCAP_ROOT}/lib 
             --with-dcap-incdir=${DCAP_ROOT}/include
             --disable-pgsql
             --disable-mysql
             --disable-xml ${EXTRA_CONFIG_ARGS}"

case $(uname)-$(uname -m) in
  Linux-x86_64)
    ./configure linuxx8664gcc $CONFIG_ARGS --with-rfio-libdir=${CASTOR_ROOT}/lib --with-rfio-incdir=${CASTOR_ROOT}/include/shift --with-castor-libdir=${CASTOR_ROOT}/lib --with-castor-incdir=${CASTOR_ROOT}/include/shift ;; 
  Linux-i*86)
    ./configure linux  $CONFIG_ARGS --with-rfio-libdir=${CASTOR_ROOT}/lib --with-rfio-incdir=${CASTOR_ROOT}/include/shift --with-castor-libdir=${CASTOR_ROOT}/lib --with-castor-incdir=${CASTOR_ROOT}/include/shift ;;
  Darwin*)
    case %cmsplatf in
    *_ia32_* ) 
      comparch=i386 ;;
    *_amd64_* )
      comparch=x86_64 ;;
    * ) 
      comparch=ppc ;;
    esac
    export CC="gcc -arch $comparch" CXX="g++ -arch $comparch"
    ./configure macosx $CONFIG_ARGS --with-cc="$CC" --with-cxx="$CXX" --disable-rfio --disable-builtin_afterimage ;;
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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
# rootcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcore.xml
  <tool name="rootcore" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Tree"/>
    <lib name="Net"/>
    <lib name="Thread"/>
    <lib name="MathCore"/>
    <lib name="RIO"/>
    <lib name="Core"/>
    <lib name="Cint"/>
    <client>
      <environment name="ROOTCORE_BASE" default="%i"/>
      <environment name="LIBDIR" default="$ROOTCORE_BASE/lib"/>
      <environment name="INCLUDE" default="$ROOTCORE_BASE/include"/>
      <environment name="INCLUDE" default="$ROOTCORE_BASE/cint"/>
    </client>
    <runtime name="PATH" value="$ROOTCORE_BASE/bin" type="path"/>
    <runtime name="ROOTSYS" value="$ROOTCORE_BASE/"/>
    <runtime name="PYTHONPATH" value="$ROOTCORE_BASE/lib" type="path"/>
    <use name="sockets"/>
    <use name="pcre"/>
    <use name="zlib"/>
  </tool>
EOF_TOOLFILE

# root toolfile, alias for rootphysics. Using rootphysics is preferred.
cat << \EOF_TOOLFILE >%i/etc/scram.d/root.xml
  <tool name="root" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <use name="rootphysics"/>
  </tool>
EOF_TOOLFILE

# roothistmatrix toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothistmatrix.xml
  <tool name="roothistmatrix" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Hist"/>
    <lib name="Matrix"/>
    <use name="ROOTCore"/>
  </tool>
EOF_TOOLFILE

# rootgpad toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgpad.xml
  <tool name="rootgpad" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Gpad"/>
    <lib name="Graf"/>
    <use name="roothistmatrix"/>
  </tool>
EOF_TOOLFILE

# rootphysics toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootphysics.xml
  <tool name="rootphysics" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Physics"/>
    <use name="roothistmatrix"/>
  </tool>
EOF_TOOLFILE

# rootgraphics toolfile, identical to old "root" toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgraphics.xml
  <tool name="rootgraphics" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="TreePlayer"/>
    <lib name="Graf3d"/>
    <lib name="Postscript"/>
    <use name="rootgpad"/>
  </tool>
EOF_TOOLFILE

# rootcintex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcintex.xml
  <tool name="rootcintex" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Cintex"/>
    <use name="ROOTRflx"/>
    <use name="ROOTCore"/>
  </tool>
EOF_TOOLFILE

# rootinteractive toolfile (GQt/qt lib dependencies
# have been moved to rootqt.xml)
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootinteractive.xml
  <tool name="rootinteractive" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Rint"/>
    <lib name="Gui"/>
    <use name="libjpg"/>
    <use name="libpng"/>
    <use name="rootgpad"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/rootqt.xml
  <tool name="rootqt" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="GQt"/>
    <use name="qt"/>
  </tool>
EOF_TOOLFILE

# rootmath toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmath.xml
  <tool name="rootmath" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="GenVector"/>
    <lib name="MathMore"/>
    <use name="ROOTCore"/>
    <use name="gsl"/>
  </tool>
EOF_TOOLFILE

# rootminuit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit.xml
  <tool name="rootminuit" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Minuit"/>
    <use name="rootgpad"/>
  </tool>
EOF_TOOLFILE

# rootminuit2 toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit2.xml
  <tool name="rootminuit2" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Minuit2"/>
    <use name="rootgpad"/>
  </tool>
EOF_TOOLFILE

# rootrflx toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrflx.xml
  <tool name="rootrflx" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Reflex"/>
    <client>
      <environment name="ROOTRFLX_BASE" default="%i"/>
      <environment name="LIBDIR" default="$ROOTRFLX_BASE/lib"/>
      <environment name="INCLUDE" default="$ROOTRFLX_BASE/include"/>
    </client>
    <runtime name="PATH" value="$ROOTRFLX_BASE/bin" type="path"/>
    <runtime name="ROOTSYS" value="$ROOTRFLX_BASE/"/>
    <runtime name="GENREFLEX" value="$ROOTRFLX_BASE/bin/genreflex"/>
    <use name="sockets"/>
    <use name="gccxml"/>
  </tool>
EOF_TOOLFILE

# roothtml toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothtml.xml
  <tool name="roothtml" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="Html"/>
    <use name="rootgpad"/>
  </tool>
EOF_TOOLFILE

# rootmlp toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmlp.xml
  <tool name="rootmlp" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="MLP"/>
    <use name="RootGraphics"/>
  </tool>
EOF_TOOLFILE

# roottmva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roottmva.xml
  <tool name="roottmva" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="TMVA"/>
    <use name="ROOTMLP"/>
    <use name="rootminuit"/>
  </tool>
EOF_TOOLFILE

# rootthread toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootthread.xml
  <tool name="rootthread" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <use name="ROOTCore"/>
  </tool>
EOF_TOOLFILE

%post
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $(find $RPM_INSTALL_PREFIX/%pkgrel/etc/scram.d -type f)

