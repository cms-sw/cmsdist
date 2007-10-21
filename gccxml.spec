### RPM external gccxml 0.6.0-CMS8

Requires: cmake
Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
Patch0: gccxml1
Patch1: gccxml2
Patch2: gccxml3
Patch3: gccxml4

%prep
%setup -n %{n}-%{realversion}
#%patch1 -p1 
%patch4 -p1 

%build
mkdir gccxml-build
cd gccxml-build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%i ..
make %makeprocesses

%install
cd gccxml-build
make install
cd %i
#patch -p1 <%{_sourcedir}/gccxml1
#patch -p1 <%{_sourcedir}/gccxml3

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<Client>
 <Environment name=GCCXML_BASE default="%i"></Environment>
</Client>
<Runtime name=PATH value="$GCCXML_BASE/bin" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}share/gccxml-0.6/gccxml_config
%{relocateConfig}etc/scram.d/%n
