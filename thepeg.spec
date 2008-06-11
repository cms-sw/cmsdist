### RPM external thepeg 1.2.0
Source: http://www.thep.lu.se/~leif/ThePEG/ThePEG-%{realversion}.tgz
Patch0: thepeg-1.2.0-LHAPDF
Requires: lhapdf
Requires: gsl

%prep
%setup -q -n ThePEG-%{realversion}
%patch0 -p0
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
<Tool name=thepeg version=%v>
<Client>
 <Environment name=THEPEG_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$THEPEG_BASE/lib/ThePEG"></Environment>
 <Environment name=INCLUDE default="$THEPEG_BASE/include"></Environment>
</Client>
<lib name=ThePEG>
<use name=lhapdf>
<use name=gsl>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
%{relocateConfig}lib/ThePEG/ACDCSampler.la
%{relocateConfig}lib/ThePEG/BreitWignerMass.la
%{relocateConfig}lib/ThePEG/ColourPairDecayer.la
%{relocateConfig}lib/ThePEG/DalitzDecayer.la
%{relocateConfig}lib/ThePEG/FixedCMSLuminosity.la
%{relocateConfig}lib/ThePEG/GaussianPtGenerator.la
%{relocateConfig}lib/ThePEG/GRV94L.la
%{relocateConfig}lib/ThePEG/GRV94M.la
%{relocateConfig}lib/ThePEG/GRVBase.la
%{relocateConfig}lib/ThePEG/KTClus.la
%{relocateConfig}lib/ThePEG/LeptonLeptonPDF.la
%{relocateConfig}lib/ThePEG/LeptonLeptonRemnant.la
%{relocateConfig}lib/ThePEG/LesHouches.la
%{relocateConfig}lib/ThePEG/libThePEG.la
%{relocateConfig}lib/ThePEG/LWHFactory.la
%{relocateConfig}lib/ThePEG/MadGraphReader.la
%{relocateConfig}lib/ThePEG/MEee2gZ2qq.la
%{relocateConfig}lib/ThePEG/MENCDIS.la
%{relocateConfig}lib/ThePEG/MEQCD.la
%{relocateConfig}lib/ThePEG/MultiEventGenerator.la
%{relocateConfig}lib/ThePEG/O1AlphaS.la
%{relocateConfig}lib/ThePEG/OmegaPhi3PiDecayer.la
%{relocateConfig}lib/ThePEG/Onium3GDecayer.la
%{relocateConfig}lib/ThePEG/QuarksToHadronsDecayer.la
%{relocateConfig}lib/ThePEG/ReweightConstant.la
%{relocateConfig}lib/ThePEG/ReweightMinPT.la
%{relocateConfig}lib/ThePEG/SimpleAlphaEM.la
%{relocateConfig}lib/ThePEG/SimpleDISCut.la
%{relocateConfig}lib/ThePEG/SimpleFlavour.la
%{relocateConfig}lib/ThePEG/SimpleKTCut.la
%{relocateConfig}lib/ThePEG/SimpleZGenerator.la
%{relocateConfig}lib/ThePEG/StandardCKM.la
%{relocateConfig}lib/ThePEG/Tau2HadronsDecayer.la
%{relocateConfig}lib/ThePEG/TestLHAPDF.la
%{relocateConfig}lib/ThePEG/ThePEGStrategy.la
%{relocateConfig}lib/ThePEG/V2LeptonsCut.la
%{relocateConfig}lib/ThePEG/V2PPDecayer.la
%{relocateConfig}lib/ThePEG/WeakToHadronsDecayer.la
%{relocateConfig}lib/ThePEG/XSecCheck.la

