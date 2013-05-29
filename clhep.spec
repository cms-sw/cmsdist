### RPM external clhep 2.0.4.6
Source: http://proj-clhep.web.cern.ch/proj-clhep/DISTRIBUTION/distributions/%n-%realversion.tgz
Patch: clhep-2.0.4.2-no-virtual-inline

%prep
%setup -n %realversion/CLHEP
# Apply the patch only for MacOSX and gcc45 (test builds as of Dec2010)
# (Technically these aren't guaranteed to be mutually exclusive, but in
# practice they are at the moment.)
case %gccver in
  4.5.*)
%patch -p1
  ;;
esac
case %cmsplatf in 
  osx*)
%patch -p1
  ;;
esac


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
