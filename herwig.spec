### RPM external herwig 6.510
Source: http://cern.ch/service-spi/external/MCGenerators/distribution/%{n}-%{realversion}-src.tgz
Requires: lhapdf

%prep
%setup -q -n %n/%{realversion}
# Danger - herwig doesn't actually need the hepmc, clhep,lhapdf 
# that appear to be used in the configure
./configure --enable-shared

%build
make 

# then hack include area as jimmy depends on missing header file..
cd include
ln -sf HERWIG65.INC herwig65.inc

%install
tar -c lib include | tar -x -C %i
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=herwig version=%v>
<lib name=herwig>
<lib name=herwig_dummy>
<Client>
 <Environment name=HERWIG_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HERWIG_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HERWIG_BASE/include"></Environment>
</Client>
<use name=f77compiler>
<use name=lhapdf>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

