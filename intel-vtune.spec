### RPM external intel-vtune 2017.0.2.478468
## NOCOMPILER

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/intel-vtune.xml
<tool name="intel-vtune" version="%{realversion}">
  <info url="https://software.intel.com/en-us/intel-vtune-amplifier-xe"/>
  <lib name="ittnotify"/>
  <client>
    <environment name="INTEL_VTUNE_BASE" default="/afs/cern.ch/sw/IntelSoftware/linux/x86_64/xe2017/vtune_amplifier_xe_%{realversion}"/>
    <environment name="INCLUDE" default="$INTEL_VTUNE_BASE/include"/>
    <environment name="LIBDIR" default="$INTEL_VTUNE_BASE/lib64"/>
    <environment name="BINDIR" default="$INTEL_VTUNE_BASE/bin64"/>
  </client>
  <runtime name="PATH" value="$INTEL_VTUNE_BASE/bin64" type="path"/>
  <runtime name="VTUNE_AMPLIFIER_XE_2017_DIR" value="$INTEL_VTUNE_BASE"/>
  <runtime name="INTEL_LICENSE_FILE" value="28518@lxlicen01.cern.ch,28518@lxlicen02.cern.ch,28518@lxlicen03.cern.ch" type="path" handler="warn"/>
</tool>
EOF_TOOLFILE

%post
if [ "$CMS_INSTALL_PREFIX" = "" ] ; then CMS_INSTALL_PREFIX=$RPM_INSTALL_PREFIX; export CMS_INSTALL_PREFIX; fi
%{relocateConfig}etc/scram.d/*.xml
echo "INTEL_VTUNE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set INTEL_VTUNE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
