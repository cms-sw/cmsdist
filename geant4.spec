### RPM external geant4 9.4.p03
%define downloadv %(echo %v | cut -d- -f1)

Requires: clhep

Source0: http://geant4.cern.ch/support/source/%n.%downloadv.tar.gz

Patch0: geant-4.8.2.p01-nobanner
Patch1: geant4-9.4.p03-fix-anti-proton-bug
Patch2: geant4-9.4.p03-use-CXXFLAGS-env-variable

%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x -O2
%endif

%prep
%setup -n %n.%downloadv

%patch0 -p1 
%patch1 -p1
%patch2 -p1

%build
if [ $(uname) = Darwin ]; then
  export MACOSX_DEPLOYMENT_TARGET="10.4"
fi

# Linux? -pthread?
touch G4BuildConf.sh
echo "export CMS_CXXFLAGS='%{cms_cxxflags}'" >> G4BuildConf.sh
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
echo "export G4_NO_VERBOSE=1" >> G4BuildConf.sh
echo "export CPPVERBOSE=yes" >> G4BuildConf.sh

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
source ./G4BuildConf.sh
mkdir -p %i
tar -cf - config source | tar -C %i -xf -

make -C $G4BASE global
make -C $G4BASE includes

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

# Clean up the sources, which are not needed in the rpm
rm -rf %i/source
