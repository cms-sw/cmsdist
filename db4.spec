### RPM external db4 4.4.20-CMS19
Source: http://download.oracle.com/berkeley-db/db-%{realversion}.NC.tar.gz

%prep
%setup -n db-%{realversion}.NC
%build
mkdir obj
cd obj
../dist/configure --prefix=%{i} --disable-java --disable-tcl
make %makeprocesses
%install
cd obj
make install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="%n" version="%v">
    <lib name="db"/>
    <client>
      <environment name="DB4_BASE" default="%i"/>
      <environment name="LIBDIR" default="$DB4_BASE/lib"/>
      <environment name="INCLUDE" default="$DB4_BASE/include"/>
      <environment name="BINDIR" default="$DB4_BASE/bin"/>
    </client>
    <runtime name="PATH" value="$BINDIR" type="path"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml

