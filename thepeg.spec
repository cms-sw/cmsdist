### RPM external thepeg 1.1.1
Source: http://www.thep.lu.se/ThePEG/ThePEG++-%{realversion}.tgz
Requires: lhapdf


%prep
%setup -q -n ThePEG++-%{realversion}/ThePEG
perl -p -i -e 's|-lLHAPDF|-llhapdf -llhapdf_dummy|' configure
perl -p -i -e 's|libLHAPDF|liblhapdf|' configure
./configure --with-LHAPDF=$LHAPDF_ROOT/lib --without-javagui --prefix=%i

%build
make

%install

make install
rm %i/share/ThePEG/Doc/fixinterfaces.pl

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=tauola version=%v>
<Client>
 <Environment name=THEPEG_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$THEPEG_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$THEPEG_BASE/include"></Environment>
</Client>
<lib name=tauola>
<lib name=pretauola>
<use name=f77compiler>
<use name=pythia6>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
