### RPM external clhep 2.0.4.2
Source: http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/distributions/%n-%realversion.tgz

%prep
%setup -n %realversion/CLHEP

%build
if [ $(uname) = Darwin ]; then
  export MACOSX_DEPLOYMENT_TARGET="10.4"
fi
CXX=g++ ./configure --prefix=%i
make

#mkdir -p shared-tmp
#cd shared-tmp
#case $(uname) in
#  Darwin ) so=dylib shared="-dynamiclib -single_module" flags= ;;
#  *      ) so=so shared="-shared" flags="-D_GNU_SOURCE" ;;
#esac
#
#set -x
#cp -i ../Evaluator/*.cc  .
#cp -i ../Evaluator/*.src .
#cp -i ../GenericFunctions/*.cc .
#cp -i ../Geometry/*.cc   .
#cp -i ../Matrix/*.cc     .
#cp -i ../Random/*.cc     .
#cp -i ../Random/*.src    .
#cp -i ../Random/*.cdat   .
#cp -i ../RandomObjects/*.cc .
#cp -i ../Vector/*.cc     .
#cp -i ../HepPDT/*.cc  .
#cp -i ../HepMC/*.cc  .
#cp -i ../StdHep/*.cc  .
#for f in *.cc; do
#  g++ -c -O2 -ansi -Wall -fPIC -I../.. $flags $f
#done
#g++ $shared -o libCLHEP-g++.%realversion.$so *.o

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
make install
#cd shared-tmp
#cp libCLHEP-g++.%realversion.$so %i/lib
#ln -s libCLHEP-g++.%realversion.$so %i/lib/libCLHEP.$so
#n -s libCLHEP-g++.%realversion.a %i/lib/libCLHEP.a
#remove the .a files
rm %i/lib/*.a
# remove the separate libs:
rm %i/lib/libCLHEP-[A-Z]*-%realversion.$so

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n.xml
  <tool name="clhep" version="%v">
    <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
    <lib name="CLHEP-%realversion"/>
    <client>
      <environment name="CLHEP_BASE" default="%i"/>
      <environment name="LIBDIR" default="$CLHEP_BASE/lib"/>
      <environment name="INCLUDE" default="$CLHEP_BASE/include"/>
    </client>
    <runtime name="CLHEP_PARAM_PATH" value="$CLHEP_BASE"/>
    <runtime name="CMSSW_FWLITE_INCLUDE_PATH" value="$CLHEP_BASE/include" type="path"/>
  </tool>
EOF_TOOLFILE

cat << \EOF_TOOLFILE >%i/etc/scram.d/clhepheader.xml
  <tool name="clhepheader" version="%v">
    <info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"/>
    <client>
      <environment name="CLHEPHEADER_BASE" default="%i"/>
      <environment name="INCLUDE"    default="$CLHEPHEADER_BASE/include"/>
    </client>
  </tool>
EOF_TOOLFILE

%post
%{relocateConfig}bin/Evaluator-config
%{relocateConfig}bin/Cast-config
%{relocateConfig}bin/GenericFunctions-config
%{relocateConfig}bin/Exceptions-config
%{relocateConfig}bin/RandomObjects-config
%{relocateConfig}bin/Geometry-config
%{relocateConfig}bin/Matrix-config
%{relocateConfig}bin/Random-config
%{relocateConfig}bin/RefCount-config
%{relocateConfig}bin/Units-config
%{relocateConfig}bin/Vector-config
%{relocateConfig}bin/clhep-config
%{relocateConfig}etc/scram.d/%n.xml
%{relocateConfig}etc/scram.d/clhepheader.xml
