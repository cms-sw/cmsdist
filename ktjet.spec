### RPM external ktjet 1.06-CMS9
Source: http://hepforge.cedar.ac.uk/hf/archive/ktjet/KtJet-%{realversion}.tar.gz
Patch1: ktjet-1.0.6-nobanner
Requires: clhep

%prep
%setup -n KtJet-%{realversion}
%patch1 -p1

%build
CPPFLAGS=" -DKTDOUBLEPRECISION -fPIC" ./configure --with-clhep=$CLHEP_ROOT --prefix=%{i}
make
%install
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=ktjet version=%v>
<info url=http://hepforge.cedar.ac.uk/ktjet></info>
<lib name=KtEvent>
<Client>
<Environment name=KTJET_BASE default="%i"></Environment>
<Environment name=LIBDIR default="$KTJET_BASE/lib"></Environment>
<Environment name=INCLUDE default="$KTJET_BASE/include"></Environment>
</Client>
<Flags CPPDEFINES="KTDOUBLEPRECISION">
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
