### RPM external geant4 7.1-p1cms
%define downloadv %(echo %v | cut -d- -f1)
## INITENV SET G4NDL_PATH %i/data/G4NDL%{g4NDLVersion}
## INITENV SET G4EMLOW_PATH %i/data/G4EMLOW%{g4EMLOWVersion}
## INITENV SET PHOTON_EVAPORATION_PATH %i/data/PhotonEvaportation%{photonEvaporationVersion}
## INITENV SET RADIATIVE_DECAY_PATH %i/data/RadiativeDecay%{radiativeDecayVersion}
# Build system fudging and some patches by Lassi A. Tuura <lat@iki.fi>
Requires: clhep
%define photonEvaporationVersion 2.0
%define g4NDLVersion 3.8
%define g4EMLOWVersion 2.2
%define radiativeDecayVersion 3.0
Source0: http://geant4.cern.ch/support/source/%n.%downloadv.tar.gz
Source1: http://geant4.cern.ch/support/source/G4NDL.%{g4NDLVersion}.tar.gz
Source2: http://geant4.cern.ch/support/source/G4EMLOW.%{g4EMLOWVersion}.tar.gz
Source3: http://geant4.cern.ch/support/source/PhotonEvaporation.%{photonEvaporationVersion}.tar.gz
Source4: http://geant4.cern.ch/support/source/RadiativeDecay.%{radiativeDecayVersion}.tar.gz
Source5: http://geant4.web.cern.ch/geant4/physics_lists/geant4.6.1/lists/Packaging.tar
Patch: geant4-g4e-and-g4tubs

%prep
%setup -n %n.%downloadv
%ifos darwin
patch0 -p7
#%patch1
%endif

%build
# Linux? -pthread?
touch G4BuildConf.sh
echo "export OS_ARCH=%{cmspatf}" >> G4BuildConf.sh
#FIXME: is this correct???
echo "export G4SYSTEM=$(uname)-g++" >> G4BuildConf.sh
echo "export G4INSTALL=%i" >> G4BuildConf.sh
echo "export G4BASE=$PWD/source" >> G4BuildConf.sh
echo "export G4WORKDIR=$PWD" >> G4BuildConf.sh
echo "export G4TMP=$PWD/tmp" >> G4BuildConf.sh
echo "export G4LIB=%i/lib" >> G4BuildConf.sh
echo "export G4LIB_BUILD_SHARED=1" >> G4BuildConf.sh
echo "export G4DEBUG=1" >> G4BuildConf.sh

echo "export G4LEVELGAMMADATA=%i/data/PhotonEvaporation/%{photonEvaporationVersion}" >> G4BuildConf.sh
echo "export G4RADIOACTIVEDATA=%i/data/RadiativeDecay%{radiativeDecayVersion}" >> G4BuildConf.sh
echo "export G4LEDATA=%i/data/G4EMLOW%{g4EMLOWVersion}" >> G4BuildConf.sh
echo "export NeutronHPCrossSections=%i/data/G4NDL%{g4NDLVersion}" >> G4BuildConf.sh

# export G4LIB_BUILD_STATIC=1
# FIXME: For OS X? export G4NO_OPTIMISE=1 // unset G4OPTIMISE
# FIXME: override CERNLIB_PATH?

echo "export CLHEP_BASE_DIR=$CLHEP_ROOT" >> G4BuildConf.sh

echo "export G4USE_STL=1" >> G4BuildConf.sh
# export G4USE_G3TOG4=1

echo "export G4UI_BUILD_TERMINAL_SESSION=1" >> G4BuildConf.sh
# export G4UI_BUILD_GAG_SESSION=1
# export G4UI_BUILD_XAW_SESSION=1
# export G4UI_BUILD_XM_SESSION=1
# export G4UI_BUILD_WO_SESSION=1

echo "export OGLHOME=/usr/X11R6" >> G4BuildConf.sh
# export OGLLIBS="-L$OGLHOME/lib -lGLU -lGL"
# export OGLFLAGS="-I$OGLHOME/include"

echo "export G4VIS_BUILD_DAWNFILE_DRIVER=1" >> G4BuildConf.sh
# export G4VIS_BUILD_DAWN_DRIVER=1
# export G4VIS_BUILD_OPENGLX_DRIVER=1
# export G4VIS_BUILD_OPENGLXM_DRIVER=1
echo "export G4VIS_BUILD_VRMLFILE_DRIVER=1" >> G4BuildConf.sh
echo "export G4VIS_BUILD_VRML_DRIVER=1" >> G4BuildConf.sh
echo "export G4VIS_BUILD_RAYTRACER_DRIVER=1" >> G4BuildConf.sh
# export G4LIB_BUILD_G3TOG4=1
source G4BuildConf.sh
mkdir -p %i
tar -cf - config source | tar -C %i -xf -
make %makeprocesses -C $G4BASE all
make %makeprocesses -C $G4BASE includes
make %makeprocesses -C $G4BASE
make %makeprocesses -C $G4BASE global
make %makeprocesses -C $G4BASE

%install
mkdir -p %i/etc
cp G4BuildConf.sh %i/etc
# Build already installed into prefix
mkdir -p %i/data
tar -C %i/data -zxvf %_sourcedir/G4NDL*.tar.gz
tar -C %i/data -zxvf %_sourcedir/G4EMLOW*.tar.gz
tar -C %i/data -zxvf %_sourcedir/Photon*.tar.gz
tar -C %i/data -zxvf %_sourcedir/Rad*.tar.gz
mkdir -p %i/share
cp -r physics_lists  %i/share 
