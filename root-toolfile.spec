### RPM lcg root-toolfile 2.1
Requires: root
Requires: gcc
%prep

%build

%install

export GCC_ROOT
export GCC_VERSION
export GCC_REALVERSION=$(gcc -dumpversion)

TARGET_TRIPLET=$(gcc -dumpmachine)
export TARGET_TRIPLET

# TODO: All additional include paths must be added at the beginning of ROOT_INCLUDE_PATH

mkdir -p %i/etc/scram.d
# root_interface toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/root_interface.xml
<tool name="root_interface" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOT_INTERFACE_BASE"     default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"                 default="$ROOT_INTERFACE_BASE/include"/>
    <environment name="LIBDIR"                  default="$ROOT_INTERFACE_BASE/lib"/>
  </client>
  <runtime name="PATH"                          value="$ROOT_INTERFACE_BASE/bin" type="path"/>
  <runtime name="ROOTSYS"                       value="$ROOT_INTERFACE_BASE/"/>
  <runtime name="ROOT_TTREECACHE_SIZE"          value="0"/>
  <runtime name="ROOT_TTREECACHE_PREFILL"       value="0"/>
  <runtime name="ROOT_INCLUDE_PATH"             value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE > %{i}/etc/scram.d/root_cxxdefaults.xml
<tool name="root_cxxdefaults" version="@TOOL_VERSION@">
  <runtime name="ROOT_GCC_TOOLCHAIN" value="@GCC_ROOT@" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/local/include" type="path" handler="warn"/>
  <runtime name="ROOT_INCLUDE_PATH" value="/usr/include"       type="path" handler="warn"/>
</tool>
EOF_TOOLFILE

# rootcling toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcling.xml
<tool name="rootcling" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Core"/>
  <client>
    <environment name="ROOTCLING_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"        default="$ROOTCLING_BASE/include"/>
  </client>
  <use name="root_interface"/>
  <use name="sockets"/>
  <use name="pcre"/>
  <use name="zlib"/>
  <use name="xz"/>
</tool>
EOF_TOOLFILE

# rootrint toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrint.xml
<tool name="rootrint" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE

# rootsmatrix toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootsmatrix.xml
<tool name="rootsmatrix" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Smatrix"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE

# rootrio toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrio.xml
<tool name="rootrio" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RIO"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE

# rootthread toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootthread.xml
<tool name="rootthread" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Thread"/>
  <use name="rootrio"/>
</tool>
EOF_TOOLFILE

# rootxmlio toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootxmlio.xml
<tool name="rootxmlio" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLIO"/>
  <use name="rootrio"/>
</tool>
EOF_TOOLFILE

# rootmathcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmathcore.xml
<tool name="rootmathcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MathCore"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE

# rootcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcore.xml
<tool name="rootcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <use name="rootmathcore"/>
  <use name="rootthread"/>
</tool>
EOF_TOOLFILE

# roothistmatrix toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothistmatrix.xml
<tool name="roothistmatrix" version="@TOOL_VERSION@"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="rootcore"/>
</tool>
EOF_TOOLFILE

# rootdataframe toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootdataframe.xml
<tool name="rootdataframe" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="ROOTDataFrame"/>
  <use name="rootcore">
  <use name="rootgraphics">
  <use name="roothistmatrix">
  <use name="rootrio">
  <use name="rootvecops"/>
</tool>
EOF_TOOLFILE

# rootvecops toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootvecops.xml
<tool name="rootvecops" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootcore">
  <lib name="ROOTVecOps"/>
</tool>
EOF_TOOLFILE

# rootspectrum toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootspectrum.xml
<tool name="rootspectrum" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Spectrum"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# rootphysics toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootphysics.xml
<tool name="rootphysics" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# root toolfile, alias for rootphysics. Using rootphysics is preferred.
cat << \EOF_TOOLFILE >%i/etc/scram.d/root.xml
<tool name="root" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootphysics"/>
  <ifversion name="^[6-9]\.">
    <flags NO_CAPABILITIES="yes"/>
  </ifversion>
</tool>
EOF_TOOLFILE

# rootgpad toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgpad.xml
<tool name="rootgpad" version="@TOOL_VERSION@"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gpad"/>
  <lib name="Graf"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# rootgraphics toolfile, identical to old "root" toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgraphics.xml
<tool name="rootgraphics" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TreePlayer"/>
  <lib name="Graf3d"/>
  <lib name="Postscript"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

# rooteg toolfile, identical to old "root" toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rooteg.xml
<tool name="rooteg" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="EG"/>
  <use name="rootgraphics"/>
</tool>
EOF_TOOLFILE

# rootpy toolfile, identical to old "root" toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootpy.xml
<tool name="rootpy" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyROOT"/>
  <use name="rootgraphics"/>
</tool>
EOF_TOOLFILE

# rootinteractive toolfile 
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootinteractive.xml
<tool name="rootinteractive" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="libjpeg-turbo"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
  <use name="rootrint"/>
</tool>
EOF_TOOLFILE

# rootmath toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmath.xml
<tool name="rootmath" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="rootcore"/>
  <use name="gsl"/>
</tool>
EOF_TOOLFILE

# rootminuit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit.xml
<tool name="rootminuit" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

# rootminuit2 toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootminuit2.xml
<tool name="rootminuit2" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Minuit2"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

# rootrflx toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrflx.xml
<tool name="rootrflx" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <client>
    <environment name="ROOTRFLX_BASE" default="@TOOL_ROOT@"/>
  </client>
  <flags GENREFLEX_GCCXMLOPT="@GENREFLEX_GCCXMLOPT@"/>
  <flags GENREFLEX_CPPFLAGS="-DCMS_DICT_IMPL -D_REENTRANT -DGNUSOURCE -D__STRICT_ANSI__"/>
  <runtime name="GENREFLEX" value="$ROOTRFLX_BASE/bin/genreflex"/>
  <use name="root_interface"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE

# roothtml toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothtml.xml
<tool name="roothtml" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Html"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

# rootmlp toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmlp.xml
<tool name="rootmlp" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="MLP"/>
  <use name="rootgraphics"/>
</tool>
EOF_TOOLFILE

# roottmva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roottmva.xml
<tool name="roottmva" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="rootmlp"/>
  <use name="rootminuit"/>
</tool>
EOF_TOOLFILE

# rootpymva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootpymva.xml
<tool name="rootpymva" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="PyMVA"/>
  <use name="roottmva"/>
  <use name="numpy-c-api"/>
</tool>
EOF_TOOLFILE

# rootxml toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootxml.xml
<tool name="rootxml" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="XMLParser"/>
  <use name="rootcore"/>
  <use name="libxml2"/>
</tool>
EOF_TOOLFILE

# rootfoam toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootfoam.xml
<tool name="rootfoam" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Foam"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# rootgeom toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgeom.xml
<tool name="rootgeom" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Geom"/>
  <use name="rootrio"/>
  <use name="rootmathcore"/>
</tool>
EOF_TOOLFILE

# rootgeompainter toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgeompainter.xml
<tool name="rootgeompainter" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GeomPainter"/>
  <use name="rootgeom"/>
  <use name="rootgraphics"/>
</tool>
EOF_TOOLFILE

# rootrgl toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootrgl.xml
<tool name="rootrgl" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RGL"/>
  <use name="rootglew"/>
  <use name="rootgui"/>
  <use name="rootinteractive"/>
  <use name="rootgraphics"/>
</tool>
EOF_TOOLFILE

# rooteve toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rooteve.xml
<tool name="rooteve" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Eve"/>
  <use name="rootgeompainter"/>
  <use name="rootrgl"/>
  <use name="rootged"/>
</tool>
EOF_TOOLFILE

# rootguihtml toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootguihtml.xml
<tool name="rootguihtml" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GuiHtml"/>
  <use name="rootgui"/>
  <use name="rootinteractive"/>
</tool>
EOF_TOOLFILE

# roofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofitcore.xml
<tool name="roofitcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFitCore"/>
  <client>
    <environment name="ROOFIT_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$ROOFIT_BASE/lib"/>
    <environment name="INCLUDE" default="$ROOFIT_BASE/include"/>
  </client>
  <runtime name="ROOFITSYS" value="$ROOFIT_BASE/"/>
  <runtime name="PATH"      value="$ROOFIT_BASE/bin" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootminuit"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

# roofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofit.xml
<tool name="roofit" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooFit"/>
  <use name="roofitcore"/>
  <use name="rootcore"/>
  <use name="rootmath"/>
  <use name="roothistmatrix"/>
</tool>
EOF_TOOLFILE

# roostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roostats.xml
<tool name="roostats" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="RooStats"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

# histfactory toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/histfactory.xml
<tool name="histfactory" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="HistFactory"/>
  <use name="roofitcore"/>
  <use name="roofit"/>
  <use name="roostats"/>
  <use name="rootcore"/>
  <use name="roothistmatrix"/>
  <use name="rootgpad"/>
  <use name="rootxml"/>
  <use name="rootfoam"/>
</tool>
EOF_TOOLFILE

#Root Ged
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootged.xml
<tool name="rootged" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Ged"/>
  <use name="rootgui"/>
</tool>
EOF_TOOLFILE

#Root GLEW
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootglew.xml
<tool name="rootglew" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GLEW"/>
</tool>
EOF_TOOLFILE

#Root Gui
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootgui.xml
<tool name="rootgui" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Gui"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

#Root X11
case %{cmsos} in
  osx*)
  cat << \EOF_TOOLFILE >%i/etc/scram.d/rootx11.xml
<tool name="rootx11" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GX11"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE
  ;;
  *)
  cat << \EOF_TOOLFILE >%i/etc/scram.d/rootx11.xml
<tool name="rootx11" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GCocoa"/>
  <use name="rootcling"/>
</tool>
EOF_TOOLFILE
  ;;
esac

case %cmsos in
  *_ia32)
    GENREFLEX_GCCXMLOPT="-m32"
  ;;
  *_amd64)
    GENREFLEX_GCCXMLOPT="-m64"
  ;;
esac
export GENREFLEX_GCCXMLOPT

## IMPORT scram-tools-post
