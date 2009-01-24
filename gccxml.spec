### RPM external gccxml 0.9.0_20081130
%define gccxmlmajorver %(echo %realversion | cut -f1 -d_)
Requires: cmake
Source: http://cern.ch/service-spi/external/tarFiles/%n-%realversion.tar.gz

%prep
%setup -n %{n}

%build
cd GCC_XML/Support
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
