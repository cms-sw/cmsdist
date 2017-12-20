### RPM external sherpa-toolfile 2.0
Requires: sherpa

%define islinux %(case $(uname -s) in (Linux) echo 1 ;; (*) echo 0 ;; esac)
%define isamd64 %(case %{cmsplatf} in (*amd64*) echo 1 ;; (*) echo 0 ;; esac)

%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/sherpa.xml
<tool name="sherpa" version="@TOOL_VERSION@">
  <lib name="SherpaMain"/>
  <lib name="ToolsMath"/>
  <lib name="ToolsOrg"/>
  <client>
    <environment name="SHERPA_BASE" default="@TOOL_ROOT@"/>
    <environment name="BINDIR" default="$SHERPA_BASE/bin"/>
    <environment name="LIBDIR" default="$SHERPA_BASE/lib/SHERPA-MC"/>
    <environment name="INCLUDE" default="$SHERPA_BASE/include/SHERPA-MC"/>
  </client>
  <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$SHERPA_BASE/include" type="path"/>
  <runtime name="SHERPA_SHARE_PATH" value="$SHERPA_BASE/share/SHERPA-MC" type="path"/>
  <runtime name="SHERPA_INCLUDE_PATH" value="$SHERPA_BASE/include/SHERPA-MC" type="path"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <runtime name="PYTHONPATH" value="$SHERPA_BASE/lib/python@PYTHONV@/site-packages" type="path"/>
  <runtime name="SHERPA_LIBRARY_PATH" value="$SHERPA_BASE/lib/SHERPA-MC" type="path"/>
  <use name="HepMC"/>
  <use name="lhapdf"/>
  <use name="qd"/>
  <use name="blackhat"/>
  <use name="fastjet"/>
  <use name="sqlite"/>
  <use name="openmpi"/>
%if %islinux
%if %isamd64
  <use name="openloops"/>
%endif # isamd64
%endif # islinux
</tool>
EOF_TOOLFILE

export PYTHONV=$(echo $PYTHON_VERSION | cut -f1,2 -d.)

## IMPORT scram-tools-post
