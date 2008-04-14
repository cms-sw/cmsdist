### RPM external gccxml 0.7.0_20070615-CMS20
%define gccxmlmajorver %(echo %realversion | cut -f1,2 -d.)
Requires: cmake
# The following are needed for 0.6.0 
#Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
#Patch1: gccxml1
#Patch2: gccxml2
#Patch3: gccxml3
#Patch4: gccxml4
# The following are needed for 0.7.0_20070615
Source: http://www.gccxml.org/files/v0.6/%n-%realversion.tar.gz
Patch5: gccxml-0.7.0-version

%prep
#%setup -n %{n}-%{realversion}   # for 0.6.0
%setup -n %{n}
#%patch2 -p1 
%patch5 -p1 

%build
cd GCC_XML/Support
# The following are needed for 0.6.0
#patch -p3 <%{_sourcedir}/gccxml1
#patch -p3 <%{_sourcedir}/gccxml3
#patch -p3 <%{_sourcedir}/gccxml4
cd ../../
mkdir gccxml-build
cd gccxml-build
cmake -DCMAKE_INSTALL_PREFIX:PATH=%i ..
make %makeprocesses

%install
cd gccxml-build
make install
cd %i

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
