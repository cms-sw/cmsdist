### RPM external clhep 1.9.2.2
Source: http://proj-clhep.web.cern.ch/proj-clhep/%n-%v.tgz

%prep
%setup -n %v/CLHEP

%build
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
