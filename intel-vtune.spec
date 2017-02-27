### RPM external intel-vtune 2017.2.0.499904
## NOCOMPILER

%prep

%build

%install
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/intel-vtune.xml
<tool name="intel-vtune" version="%{realversion}">
  <info url="https://software.intel.com/en-us/intel-vtune-amplifier-xe"/>
  <client>
    <environment name="INTEL_VTUNE_BASE" default="/cvmfs/projects.cern.ch/intelsw/psxe/linux/x86_64/2017/vtune_amplifier_xe_%{realversion}"/>
    <environment name="BINDIR" default="$INTEL_VTUNE_BASE/bin64"/>
  </client>
  <runtime name="PATH" value="$INTEL_VTUNE_BASE/bin64" type="path"/>
  <runtime name="VTUNE_AMPLIFIER_XE_2017_DIR" value="$INTEL_VTUNE_BASE"/>
</tool>
EOF_TOOLFILE

%post
if [ "$CMS_INSTALL_PREFIX" = "" ] ; then CMS_INSTALL_PREFIX=$RPM_INSTALL_PREFIX; export CMS_INSTALL_PREFIX; fi
%{relocateConfig}etc/scram.d/*.xml
echo "INTEL_VTUNE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set INTEL_VTUNE_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
