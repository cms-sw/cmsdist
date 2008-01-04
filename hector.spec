### RPM external hector 1_3_2-CMS19
%define rname Hector
%define realversion %(echo %v | cut -d- -f1 )
Requires: root
Source: http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/%{rname}_%{realversion}.tbz
Patch0: hector-1.3.2-fPIC
Patch1: hector-1.3.2-root-includes
Patch2: hector-1.3.2-TView

%prep
%setup -q -n %{rname}
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 

%build
make

%install
tar -c . | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=Hector version=%v>
<info url=http://www.fynu.ucl.ac.be/themes/he/ggamma/hector/></info>
<lib name=Hector>
<client>
 <Environment name=HECTOR_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HECTOR_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HECTOR_BASE/include"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
