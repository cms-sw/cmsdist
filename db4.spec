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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Lib name=db>
<Client>
 <Environment name=DB4_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$DB4_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$DB4_BASE/include"></Environment>
 <Environment name=BINDIR default="$DB4_BASE/bin"></Environment>
</Client>
<Runtime name=PATH value="$BINDIR" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

