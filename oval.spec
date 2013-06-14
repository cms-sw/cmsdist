### RPM external oval 3_5_0
Source: http://oval.in2p3.fr/%{n}_%{realversion}.tar.gz
Provides: perl(ActiveDoc::GroupChecker)
%prep
%setup -n %realversion

%build
%install
tar -cf - . | tar -C %i -xf -
find %i -type d -name CVS -print | xargs rm -fr

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <client>
      <environment name="OVAL_BASE" default="%i"/>
    </client>
  </tool>
EOF_TOOLFILE

case %cmsplatf in
slc3_* | slc4_* )
echo '<Runtime name=OVAL_FLAVOR value="Linux">' >> %i/etc/scram.d/%n
;;
osx* )
echo '<Runtime name=OVAL_FLAVOR value="osx">' >> %i/etc/scram.d/%n
;;
esac
cat << \EOF_TOOLFILE >>%i/etc/scram.d/%n
<runtime name=PATH value="$OVAL_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
