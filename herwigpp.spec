### RPM external herwigpp 2.2.0
Source: http://projects.hepforge.org/herwig/files/Herwig++-%{realversion}.tar.gz
Requires: thepeg
Requires: gsl
Requires: hepmc


%prep
%setup -q -n Herwig++-%{realversion}
./configure --with-hepmc=$HEPMC_ROOT --with-gsl=$GSL_ROOT --with-thepeg=$THEPEG_ROOT --prefix=%i

%build
make %makeprocesses

%install
#tar -c -h lib include | tar -x -C %i
make install
# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=herwigpp version=%v>
<Client>
 <Environment name=HERWIGPP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$HERWIGPP_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$HERWIGPP_BASE/include"></Environment>
</Client>
<lib name=tauola>
<lib name=pretauola>
<use name=f77compiler>
<use name=pythia6>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
