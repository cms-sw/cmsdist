### RPM external fastjet 2.1.0
Source: http://www.lpthe.jussieu.fr/~salam/repository/software/fastjet/%n-%v.tgz
%prep
%setup -n %n-%v

%build
## IMPORT gcc-wrapper
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
