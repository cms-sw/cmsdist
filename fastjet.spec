### RPM external fastjet 2.3.0
Source: http://www.lpthe.jussieu.fr/~salam/repository/software/fastjet/%n-%realversion.tar.gz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet_sisconebanner

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1
./configure --enable-shared --prefix=%i

%build
make

%install
make install


# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=FastJet version=%v>
<info url=http://www.lpthe.jussieu.fr/~salam/fastjet/></info>
<lib name=SISConePlugin>
<lib name=CDFConesPlugin>
<lib name=siscone>
<lib name=fastjet>
<client>
 <Environment name=FASTJET_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$FASTJET_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$FASTJET_BASE/include"></Environment>
</client>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
