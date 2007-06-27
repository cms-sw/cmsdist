### RPM external fastjet 2.1.0-CMS3
Source: http://www.lpthe.jussieu.fr/~salam/repository/software/fastjet/%n-%realversion.tgz
Patch1: fastjet-2.1.0-nobanner

%prep
%setup -n %n-%realversion
%patch1 -p1

%build
cd src
# The following is a hack, whether it works should be checked whenever
# the version is updated from 2.1.0b1
perl -p -i -e "s|CXXFLAGS \+\=|CXXFLAGS += -fPIC|" Makefile
make
make install
cd ../plugins
make
make clean

cd ../include/fastjet
find ../../plugins/CDFCones -name "*.hh" -exec ln -sf {}  \;
find ../../plugins/SISCone -name "*.hh" -exec ln -sf {}  \;

cd ../../lib/
find ../plugins/CDFCones -name "*.a" -exec mv {} .  \;
find ../plugins/SISCone -name "*.a" -exec mv {} .  \;


%install

# Take everything including sources, makefiles, documentation and examples (only 16MB).
gtar -cv ./| gtar -x -C %i
