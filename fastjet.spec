### RPM external fastjet 2.1.0-CMS8
Source: http://www.lpthe.jussieu.fr/~salam/repository/software/fastjet/%n-%realversion.tgz
Patch1: fastjet-2.1.0-nobanner
Patch2: fastjet_sisconebanner

%prep
%setup -n %n-%realversion
%patch1 -p1
%patch2 -p1

%build
# The following is a hack, whether it works should be checked whenever
# the version is updated from 2.1.0b1
perl -p -i -e "s|CXXFLAGS \+\= \-O3|CXXFLAGS += -fPIC -O3|" Makefile
cd src
make
make install
cd ../plugins
perl -p -i -e "s|CFLAGS  \=|CFLAGS  = -fPIC|" SISCone/siscone/src/Makefile
perl -p -i -e "s|^CXXFLAGSmidpoint \=|CXXFLAGSmidpoint = -fPIC|" CDFCones/CDFcode/Makefile
make
make clean

cd ../include/fastjet
find ../../plugins/CDFCones -name "*.hh" -exec ln -sf {}  \;
find ../../plugins/SISCone -name "*.hh" -exec ln -sf {}  \;

cd ../../lib/
find ../plugins/CDFCones -name "*.a" -exec mv {} .  \;
find ../plugins/SISCone -name "*.a" -exec mv {} .  \;


%install

# Take everything including sources, makefiles, documentation and examples (only 16MB).
gtar -cv ./| gtar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=FastJet version=%v>
<info url=http://www.lpthe.jussieu.fr/~salam/fastjet/></info>
<lib name=SISConePlugin>
<lib name=CDFConesPlugin>
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
