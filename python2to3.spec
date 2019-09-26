### RPM external python2to3 1.0
Requires: python python3
%prep
%build
%install
mkdir -p %i/etc/scram.d %i/bin
pushd %i/bin
  ln -s $(which python3 | sed 's|^%{cmsroot}/|../../../../../|') python
popd
cat << \EOF_TOOLFILE >%i/etc/scram.d/python2to3.xml
<tool name="python2to3" version="%{realversion}">
  <client>
    <environment name="PYTHON2TO3_BASE" default="%{i}"/>
  </client>
  <runtime name="PATH" value="$PYTHON2TO3_BASE/bin" type="path"/>
  <use name="python"/>
  <use name="python3"/>
</tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/python2to3.xml
