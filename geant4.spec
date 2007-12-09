### RPM external geant4 9.1.cand03-CMS18
%define downloadv %(echo %v | cut -d- -f1)
# Build system fudging and some patches by Lassi A. Tuura <lat@iki.fi>  
Provides: /bin/awk
Requires: clhep

%define photonEvaporationVersion 2.0

# FIXME: g4NDLVersion 3.12 must be used, but tarball for it 
#        is not available yet, so we take 3.11 . NR 2007/12/06

%define g4NDLVersion 3.11
%define g4ElasticScatteringVersion 1.1
%define g4EMLOWVersion 5.1
%define radioactiveDecayVersion 3.2

#Source0: http://geant4.cern.ch/support/source/%n.%downloadv.tar.gz

Source0: cvs://:kserver:ratnik@geant4.cvs.cern.ch:/cvs/Geant4?tag=-rgeant4-09-01-cand-03&module=geant4&output=/%n.%downloadv.tar.gz
Source1: http://geant4.cern.ch/support/source/G4NDL.%{g4NDLVersion}.tar.gz
Source2: http://geant4.cern.ch/support/source/G4EMLOW.%{g4EMLOWVersion}.tar.gz
Source3: http://geant4.cern.ch/support/source/PhotonEvaporation.%{photonEvaporationVersion}.tar.gz
Source4: http://geant4.cern.ch/support/source/G4RadioactiveDecay.%{radioactiveDecayVersion}.tar.gz
Source5: http://geant4.cern.ch/support/source/G4ELASTIC.%{g4ElasticScatteringVersion}.tar.gz

#Patch: geant-4.8.2.p01-nobanner
Patch1: geant4.9.1.cand03-debug-on

%prep
%setup -n %n
pwd
#%patch0 -p1 
%patch1 -p1 

%build
if [ $(uname) = Darwin ]; then
  export MACOSX_DEPLOYMENT_TARGET="10.4"
fi
# Linux? -pthread?
touch G4BuildConf.sh
echo "export OS_ARCH=%{cmsplatf}" >> G4BuildConf.sh
#FIXME: is this correct???
echo "export G4SYSTEM=$(uname)-g++" >> G4BuildConf.sh
echo "export G4INSTALL=%i" >> G4BuildConf.sh
echo "export G4BASE=$PWD/source" >> G4BuildConf.sh
echo "export G4WORKDIR=$PWD" >> G4BuildConf.sh
echo "export G4TMP=$PWD/tmp" >> G4BuildConf.sh
echo "export G4LIB=%i/lib" >> G4BuildConf.sh
echo "export G4LIB_BUILD_SHARED=1" >> G4BuildConf.sh
echo "unset G4DEBUG" >> G4BuildConf.sh
echo "export CPPVERBOSE=yes" >> G4BuildConf.sh

echo "export G4LEVELGAMMADATA=%i/data/PhotonEvaporation/%{photonEvaporationVersion}" >> G4BuildConf.sh
echo "export G4RADIOACTIVEDATA=%i/data/RadioactiveDecay%{radioactiveDecayVersion}" >> G4BuildConf.sh
echo "export G4LEDATA=%i/data/G4EMLOW%{g4EMLOWVersion}" >> G4BuildConf.sh
# G4ELASTIC is not needed from 8.2 onward
#echo "export G4ELASTIC=%i/data/G4ELASTIC%{g4ElasticScatteringVersion}" >> G4BuildConf.sh

# From Gabriele Cosmo: The variable name 'NeutronHPCrossSections' is replaced by
# 'G4NEUTRONHPDATA' starting from version 9.0.
echo "export NeutronHPCrossSections=%i/data/G4NDL%{g4NDLVersion}" >> G4BuildConf.sh

# export G4LIB_BUILD_STATIC=1
# FIXME: For OS X? export G4NO_OPTIMISE=1 // unset G4OPTIMISE
# FIXME: override CERNLIB_PATH?

echo "export CLHEP_BASE_DIR=$CLHEP_ROOT" >> G4BuildConf.sh

echo "export G4USE_STL=1" >> G4BuildConf.sh
# export G4USE_G3TOG4=1

# G4UI_BUILD_TERMINAL_SESSION is the default:
echo "export G4UI_BUILD_TERMINAL_SESSION=1" >> G4BuildConf.sh
# export G4UI_BUILD_GAG_SESSION=1
# export G4UI_BUILD_XAW_SESSION=1
# export G4UI_BUILD_XM_SESSION=1
# export G4UI_BUILD_WO_SESSION=1

# FIXME: this will not work on osx!
echo "export OGLHOME=/usr/X11R6" >> G4BuildConf.sh
# export OGLLIBS="-L$OGLHOME/lib -lGLU -lGL"
# export OGLFLAGS="-I$OGLHOME/include"

# G4VIS_BUILD_DAWNFILE_DRIVER is the default
echo "export G4VIS_BUILD_DAWNFILE_DRIVER=1" >> G4BuildConf.sh
# export G4VIS_BUILD_DAWN_DRIVER=1
# export G4VIS_BUILD_OPENGLX_DRIVER=1
# export G4VIS_BUILD_OPENGLXM_DRIVER=1
# echo "export G4VIS_BUILD_VRMLFILE_DRIVER=1" >> G4BuildConf.sh
# echo "export G4VIS_BUILD_VRML_DRIVER=1" >> G4BuildConf.sh
# echo "export G4VIS_BUILD_RAYTRACER_DRIVER=1" >> G4BuildConf.sh
# export G4LIB_BUILD_G3TOG4=1
source G4BuildConf.sh
mkdir -p %i
tar -cf - config source | tar -C %i -xf -

make %makeprocesses -C $G4BASE global
make %makeprocesses -C $G4BASE includes

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
mkdir -p %i/etc
cp G4BuildConf.sh %i/etc
mv %i/lib/$(uname)-g++/*.$so %i/lib
# The following file does not appear to exist after this spec file was 
# switched # to use the subsystem libraries instead of the individual ones, 
# so comment # it for now
#mv %i/lib/$(uname)-g++/libname.map %i/lib
rm -rf %i/lib/$(uname)-g++
# Build already installed into prefix
mkdir -p %i/data
tar -C %i/data -zxvf %_sourcedir/G4NDL*.tar.gz
tar -C %i/data -zxvf %_sourcedir/G4EMLOW*.tar.gz
tar -C %i/data -zxvf %_sourcedir/Photon*.tar.gz
tar -C %i/data -zxvf %_sourcedir/G4Rad*.tar.gz
#

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.1>
<Tool name=GEANT4 version=%v>
<info url=http://wwwinfo.cern.ch/asd/geant4/geant4.html></info>
<lib name=G4digits_hits>
<lib name=G4error_propagation>
<lib name=G4event>
<lib name=G4FR>
<lib name=G4geometry>
<lib name=G4global>
<lib name=G4graphics_reps>
<lib name=G4intercoms>
<lib name=G4interfaces>
<lib name=G4materials>
<lib name=G4modeling>
<lib name=G4parmodels>
<lib name=G4particles>     
<lib name=G4persistency>
<lib name=G4physicslists>
<lib name=G4processes>
<lib name=G4RayTracer>
<lib name=G4readout>
<lib name=G4run>
<lib name=G4tracking>
<lib name=G4track>
<lib name=G4Tree>
<lib name=G4visHepRep>
<lib name=G4vis_management>
<lib name=G4visXXX>
<lib name=G4VRML>
<Client>
<Environment name=GEANT4_BASE default="%i"></Environment>
<Environment name=G4SRC default="$GEANT4_BASE/source"></Environment>
<Environment name=LIBDIR default="$GEANT4_BASE/lib"></Environment>
<Environment name=G4LIB value="$LIBDIR"></Environment>
<Environment name=INCLUDE default="$GEANT4_BASE/include"></Environment>
</Client>
<use name=clhep>
<Flags CPPDEFINES="G4USE_STD_NAMESPACE GNU_GCC G4V9">
<Runtime name=G4LEVELGAMMADATA value="$GEANT4_BASE/data/PhotonEvaporation2.0" type=path>
<Runtime name=NeutronHPCrossSections value="$GEANT4_BASE/data/G4NDL3.11" type=path>
<Runtime name=G4RADIOACTIVEDATA value="$GEANT4_BASE/data/RadioactiveDecay3.2" type=path>
<Runtime name=G4LEDATA value="$GEANT4_BASE/data/G4EMLOW5.1" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n
