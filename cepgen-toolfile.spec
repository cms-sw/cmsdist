### RPM external cepgen-toolfile 1.0
Requires: cepgen
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/cepgen.xml
<tool name="cepgen" version="@TOOL_VERSION@">
  <info url="https://cepgen.hepforge.org/"/>
  <lib name="CepGen"/>
  <lib name="CepGenHepMC2"/>
  <lib name="CepGenLHAPDF"/>
  <lib name="CepGenProcesses"/>
  <lib name="CepGenPythia6"/>
  <client>
    <environment name="CEPGEN_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR" default="$CEPGEN_BASE/lib64"/>
    <environment name="INCLUDE" default="$CEPGEN_BASE/include"/>
  </client>
  <runtime name="PATH" value="$CEPGEN_BASE/bin" type="path"/>
  <runtime name="CEPGEN_PATH" value="$CEPGEN_BASE/share/CepGen"/>
  <use name="gsl"/>
  <use name="OpenBLAS"/>
  <use name="hepmc"/>
  <use name="lhapdf"/>
  <use name="pythia6"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
