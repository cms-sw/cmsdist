### RPM external lcov 1.9
## NOCOMPILER
Source: http://heanet.dl.sourceforge.net/sourceforge/ltp/%n-%realversion.tar.gz
Patch0: lcov-merge-files-in-same-dir

%prep
%setup -n %n-%realversion
%patch0 -p1

%build
make %makeprocesses

%install
make PREFIX=%i BIN_DIR=%i/bin install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
<tool name="lcov" version="%v">
  <info url="http://ltp.sourceforge.net/coverage/lcov.php"/>                                                                                                                                                                                                                                                             
  <client>
    <environment name="LCOV_BASE" default="%i"/>
  </client>
  <runtime name="PATH" value="$LCOV_BASE/bin" type="path"/>
</tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
