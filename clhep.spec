### RPM external clhep 1.9.2.3
Requires: gcc-wrapper
Source: http://proj-clhep.web.cern.ch/proj-clhep/%n-%v.tgz

%prep
%setup -n %v/CLHEP

%build
## IMPORT gcc-wrapper
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
#g++ $shared -o libCLHEP-g++.%v.$so *.o

%install
case $(uname) in Darwin ) so=dylib ;; * ) so=so ;; esac
make install
#cd shared-tmp
#cp libCLHEP-g++.%v.$so %i/lib
#ln -s libCLHEP-g++.%v.$so %i/lib/libCLHEP.$so
#n -s libCLHEP-g++.%v.a %i/lib/libCLHEP.a
%post
%{relocateConfig}bin/Evaluator-config
%{relocateConfig}bin/Cast-config
%{relocateConfig}bin/GenericFunctions-config
%{relocateConfig}bin/Exceptions-config
%{relocateConfig}bin/RandomObjects-config
%{relocateConfig}bin/Geometry-config
%{relocateConfig}bin/HepMC-config
%{relocateConfig}bin/HepPDT-config
%{relocateConfig}bin/Matrix-config
%{relocateConfig}bin/Random-config
%{relocateConfig}bin/RefCount-config
%{relocateConfig}bin/StdHep-config
%{relocateConfig}bin/Units-config
%{relocateConfig}bin/Vector-config
%{relocateConfig}bin/clhep-config
