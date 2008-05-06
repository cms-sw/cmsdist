### RPM external thepeg 1.2.0
Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
Requires: lhapdf
Requires: gsl

%prep
%setup -q -n ThePEG-%{realversion}
perl -p -i -e 's|-lLHAPDF|-llhapdf -llhapdf_dummy|' configure
perl -p -i -e 's|libLHAPDF|liblhapdf|' configure
./configure --with-LHAPDF=$LHAPDF_ROOT/lib --without-javagui --prefix=%i --with-gsl=$GSL_ROOT

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
<lib name=thepeg>
<use name=lhapdf>
<use name=gsl>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
