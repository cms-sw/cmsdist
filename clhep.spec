### RPM external clhep 1.9.3.1-CMS1
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

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<info url="http://wwwinfo.cern.ch/asd/lhc++/clhep"></info>
<lib name=CLHEP-Cast-%realversion>
<lib name=CLHEP-Evaluator-%realversion>
<lib name=CLHEP-Exceptions-%realversion>
<lib name=CLHEP-GenericFunctions-%realversion>
<lib name=CLHEP-Geometry-%realversion>
<lib name=CLHEP-Matrix-%realversion>
<lib name=CLHEP-Random-%realversion>
<lib name=CLHEP-RandomObjects-%realversion>
<lib name=CLHEP-RefCount-%realversion>
<lib name=CLHEP-Vector-%realversion>
<Client>
 <Environment name=CLHEP_BASE default="%i"></Environment>
 <Environment name=LIBDIR default="$CLHEP_BASE/lib"></Environment>
 <Environment name=INCLUDE default="$CLHEP_BASE/include"></Environment>
</Client>
<Runtime name=CLHEP_PARAM_PATH value="$CLHEP_BASE">
</Tool>
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
%{relocateConfig}etc/scram.d/%n
