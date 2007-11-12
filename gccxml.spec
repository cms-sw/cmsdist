### RPM external gccxml 0.6.0-CMS18
# or gccxml 0.7.0_20070615-CMS18
%define gccxmlmajorver %(echo %realversion | cut -f1,2 -d.)
Requires: cmake
# The next 5 lines are needed for 0.6.0 
Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
Patch1: gccxml1
Patch2: gccxml2
Patch3: gccxml3
Patch4: gccxml4
# The next 2 lines are needed for 0.7.0_20070615
#Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
#Patch5: gccxml-0.7.0-version

%prep
%setup -n %{n}-%{realversion}   # for 0.6.0 (this and next line)
%patch2 -p1 
# For 0.7.0 (next 2 lines)
#%setup -n %{n}
#%patch5 -p1 

%build
mkdir gccxml-build
cd gccxml-build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%i ..
make %makeprocesses

%install
cd gccxml-build
make install
cd %i
# For 0.6.0 (next 4 lines)
patch -p1 <%{_sourcedir}/gccxml1
patch -p1 <%{_sourcedir}/gccxml3
cd share/gccxml-0.6
patch -p3 <%{_sourcedir}/gccxml4


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
%{relocateConfig}share/gccxml-%{gccxmlmajorver}/gccxml_config
%{relocateConfig}etc/scram.d/%n
