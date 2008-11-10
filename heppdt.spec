### RPM external heppdt 3.03.00
Source: http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-%{realversion}.tar.gz
Patch1: heppdt-2.03.00-nobanner

%prep
%setup -q -n HepPDT-%{realversion}
%patch1 -p1
./configure  --prefix=%{i} 

%build
make 

%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=HepPDT version=%v>
<lib name=HepPDT>
<lib name=HepPID>
<Client>
 <Environment name=HEPPDT_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HEPPDT_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HEPPDT_BASE/include"></Environment>
</Client>
<Runtime name=HEPPDT_PARAM_PATH value="$HEPPDT_BASE">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
