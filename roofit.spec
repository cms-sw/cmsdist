### RPM lcg roofit 5.28.00
%define svnTag %(echo %realversion | tr '.' '-')
Source0: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz
Source1: svn://root.cern.ch/svn/root/tags/v%svnTag/tutorials/?scheme=http&module=tutorials&output=/rootutorials.tgz
Source2: roofit-5.28.00-build.sh

Patch: root-5.22-00a-roofit-silence-static-printout
Patch1: roofit-5.24-00-RooFactoryWSTool-include

Requires: root 

%prep
%setup -b0 -n roofit
%patch -p2
%patch1 -p1
%setup -D -T -b 1 -n tutorials
 
%build
#Copy over the tutorials
mkdir -p %i/tutorials/
cd ../tutorials/
cp -R roofit %i/tutorials/
cp -R roostats %i/tutorials/
cp -R histfactory %i/tutorials/

cd ../roofit/
mkdir -p %i/config
cp histfactory/config/prepareHistFactory %i/config/
cp %_sourcedir/roofit-5.28.00-build.sh build.sh
chmod +x build.sh
# Remove an extra -m64 from Wouter's build script (in CXXFLAGS and LDFLAGS)
perl -p -i -e 's|-m64 ||' build.sh
case %cmsplatf in
  osx10[0-9]_* )
# Change gawk to awk
perl -p -i -e 's|gawk|awk|' build.sh
# -soname not on osx
perl -p -i -e 's|-Wl,-soname,\S*\.so|-dynamiclib|' build.sh
  ;;
esac

./build.sh
mv build/lib %i/
mkdir %i/include
cp -r build/inc/* %i/include
# Change name of one binary by hand
mkdir %i/bin
mv build/bin/MakeModelAndMeasurements %i/bin/hist2workspace
# On macosx we cannot simply rename libraries and executables.
case %cmsos in 
  osx*)
	install_name_tool -change MakeModelAndMeasurements hist2workspace -id hist2workspace %i/bin/hist2workspace
	find %i/lib -name "*.so" -exec install_name_tool -change build/lib/libRooStats.so libRooStats.so {} \;
	find %i/lib -name "*.so" -exec install_name_tool -change build/lib/libRooFitCore.so libRooFitCore.so  {} \; 
	find %i/lib -name "*.so" -exec install_name_tool -change build/lib/libRooFit.so libRooFit.so  {} \; 
	find %i/lib -name "*.so" -exec install_name_tool -change build/lib/libHistFactory.so libHistFactory.so {} \; 
        find %i/bin -type f -exec install_name_tool -change build/lib/libRooStats.so libRooStats.so {} \;
        find %i/bin -type f -exec install_name_tool -change build/lib/libRooFitCore.so libRooFitCore.so  {} \;
        find %i/bin -type f -exec install_name_tool -change build/lib/libRooFit.so libRooFit.so  {} \;
        find %i/bin -type f -exec install_name_tool -change build/lib/libHistFactory.so libHistFactory.so {} \;
  ;;
esac

%install

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d

# rootroofitcore toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofitcore.xml
  <tool name="roofitcore" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="RooFitCore"/>
    <client>
      <environment name="ROOFIT_BASE" default="%i"/>
      <environment name="LIBDIR" default="$ROOFIT_BASE/lib"/>
      <environment name="INCLUDE" default="$ROOFIT_BASE/include"/>
    </client>
    <use name="rootcore"/>
    <use name="roothistmatrix"/>
    <use name="rootgpad"/>
    <use name="rootminuit"/>
  </tool>
EOF_TOOLFILE

# rootroofit toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roofit.xml
  <tool name="roofit" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="RooFit"/>
    <use name="roofitcore"/>
  </tool>
EOF_TOOLFILE

# rootroostats toolfile
cat << \EOF_TOOLFILE >%i/etc/scram.d/roostats.xml
  <tool name="roostats" version="%v">
    <info url="http://root.cern.ch/root/"/>
    <lib name="RooStats"/>
    <use name="roofit"/>
  </tool>
EOF_TOOLFILE

%post
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $(find $RPM_INSTALL_PREFIX/%pkgrel/etc/scram.d -type f)
