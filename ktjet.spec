### RPM external ktjet 1.06
Source: http://www.hepforge.org/archive/ktjet/KtJet-%{realversion}.tar.gz
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
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="ktjet" version="%v">
    <info url="http://hepforge.cedar.ac.uk/ktjet"/>
    <lib name="KtEvent"/>
    <client>
      <environment name="KTJET_BASE" default="%i"/>
      <environment name="LIBDIR" default="$KTJET_BASE/lib"/>
      <environment name="INCLUDE" default="$KTJET_BASE/include"/>
    </client>
    <flags cppdefines="KTDOUBLEPRECISION"/>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n.xml
