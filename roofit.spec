### RPM lcg roofit 5.34.22
%define tag 459da1ac81d51a108e851636754169a8494de6d7
%define branch cms/v5-34-22
%define github_user cms-sw
Source: git+https://github.com/%github_user/root.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz
Source1: roofit-5.28.00-build.sh

Requires: root 


%if "%{?cms_cxxflags:set}" != "set"
%define cms_cxxflags -std=c++0x
%endif

%prep
%setup -b0 -n %{n}-%{realversion}
 
%build
#Copy over the tutorials
mkdir -p %{i}/tutorials/
pushd ./tutorials
cp -R roofit %{i}/tutorials/
cp -R roostats %{i}/tutorials/
cp -R histfactory %{i}/tutorials/
popd

cd ./roofit
mkdir -p %{i}/bin
cp roostats/inc/RooStats/*.h roostats/inc/
cp histfactory/inc/RooStats/HistFactory/*.h histfactory/inc/
cp histfactory/config/prepareHistFactory %i/bin/
cp %{SOURCE1} build.sh
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
