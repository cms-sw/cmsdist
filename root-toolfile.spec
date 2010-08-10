### RPM lcg root-toolfile 1.0
Requires: root
%prep

%build

%install

mkdir -p %i/etc/scram.d
# rootcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcore.xml
<tool name="rootcore" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Tree"/>
  <lib name="Net"/>
  <lib name="Thread"/>
  <lib name="MathCore"/>
  <lib name="RIO"/>
  <lib name="Core"/>
  <lib name="Cint"/>
  <client>
    <environment name="ROOTCORE_BASE" default="@TOOL_ROOT@"/>
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
<tool name="root" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <use name="rootphysics"/>
</tool>
EOF_TOOLFILE

# roothistmatrix toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roothistmatrix.xml
<tool name="roothistmatrix" version="@TOOL_VERSION@"> 
  <info url="http://root.cern.ch/root/"/>
  <lib name="Hist"/>
  <lib name="Matrix"/>
  <use name="ROOTCore"/>
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

# rootphysics toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootphysics.xml
<tool name="rootphysics" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Physics"/>
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

# rootcintex toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootcintex.xml
<tool name="rootcintex" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Cintex"/>
  <use name="ROOTRflx"/>
  <use name="ROOTCore"/>
</tool>
EOF_TOOLFILE

# rootinteractive toolfile (GQt/qt lib dependencies
# have been moved to rootqt.xml)
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootinteractive.xml
<tool name="rootinteractive" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="Rint"/>
  <lib name="Gui"/>
  <use name="libjpg"/>
  <use name="libpng"/>
  <use name="rootgpad"/>
</tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/rootqt.xml
<tool name="rootqt" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GQt"/>
  <use name="qt"/>
</tool>
EOF_TOOLFILE

# rootmath toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootmath.xml
<tool name="rootmath" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="GenVector"/>
  <lib name="MathMore"/>
  <use name="ROOTCore"/>
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
  <lib name="Reflex"/>
  <client>
    <environment name="ROOTRFLX_BASE" default="@TOOL_ROOT@"/>
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
  <use name="RootGraphics"/>
</tool>
EOF_TOOLFILE

# roottmva toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roottmva.xml
<tool name="roottmva" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <lib name="TMVA"/>
  <use name="ROOTMLP"/>
  <use name="rootminuit"/>
</tool>
EOF_TOOLFILE

# rootthread toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/rootthread.xml
<tool name="rootthread" version="@TOOL_VERSION@">
  <info url="http://root.cern.ch/root/"/>
  <use name="ROOTCore"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
