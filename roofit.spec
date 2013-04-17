### RPM lcg roofit 5.34.05
%define svnTag %(echo %realversion | tr '.' '-')
Source0: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz
Source1: svn://root.cern.ch/svn/root/tags/v%svnTag/tutorials/?scheme=http&module=tutorials&output=/rootutorials.tgz
Source2: roofit-5.28.00-build.sh

Patch0: root-5.28-00d-roofit-silence-static-printout
Patch1: roofit-5.24-00-RooFactoryWSTool-include
Patch2: roofit-5.30.00-remove-tmath-infinity

Requires: root 


%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -b0 -n roofit
%patch0 -p2
%patch1 -p1
%patch2 -p2
%setup -D -T -b 1 -n tutorials
 
%build
#Copy over the tutorials
mkdir -p %i/tutorials/
cd ../tutorials/
cp -R roofit %i/tutorials/
cp -R roostats %i/tutorials/
cp -R histfactory %i/tutorials/

cd ../roofit/
mkdir -p %i/bin
cp roostats/inc/RooStats/*.h roostats/inc/
cp histfactory/inc/RooStats/HistFactory/*.h histfactory/inc/
cp histfactory/config/prepareHistFactory %i/bin/
cp %_sourcedir/roofit-5.28.00-build.sh build.sh
chmod +x build.sh
# Remove an extra -m64 from Wouter's build script (in CXXFLAGS and LDFLAGS)
perl -p -i -e 's|-m64||' build.sh
perl -p -i -e "s|CXXFLAGS='|CXXFLAGS='%cms_cxxflags |" build.sh
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
