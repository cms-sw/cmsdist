### RPM lcg roofit 5.27.06
%define svnTag %(echo %realversion | tr '.' '-')
Source0: svn://root.cern.ch/svn/root/tags/v%svnTag/roofit?scheme=http&module=roofit&output=/roofit.tgz
Source1: svn://root.cern.ch/svn/root/tags/v%svnTag/tutorials/?scheme=http&module=tutorials&output=/rootutorials.tgz

Patch:  roofit-5.24-00-build.sh 
Patch1: root-5.22-00a-roofit-silence-static-printout
Patch2: roofit-5.24-00-RooFactoryWSTool-include
Patch3: roofit-5.27-04-NOROOMINIMIZER

Requires: root 

%prep
%setup -b0 -n roofit
%patch -p1
%patch1 -p2
%patch2 -p1
%patch3 -p1
%setup -D -T -b 1 -n tutorials
 
%build
#Copy over the tutorials
mkdir -p %i/tutorials/
cd ../tutorials/
cp -R roofit %i/tutorials/
cp -R roostats %i/tutorials/

cd ../roofit/
chmod +x build.sh
# Remove an extra -m64 from Wouter's build script (in CXXFLAGS and LDFLAGS)
perl -p -i -e 's|-m64 ||' build.sh
# Add in a macro needed (via the NOROOMINIMIZER patch above) to avoid 
# compiling some code bits in roofit which do not build with 
# ROOT5.22/00 (5.24/00 or later is needed) in CXXFLAGS
perl -p -i -e 's|-O2 -pipe|-O2 -pipe -D__ROOFIT_NOROOMINIMIZER|' build.sh
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
