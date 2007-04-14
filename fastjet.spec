### RPM external fastjet 2.1.0b1
Source: http://www.lpthe.jussieu.fr/~salam/repository/software/fastjet/%n-%v.tgz

%prep
%setup -n %n-%v

%build
cd src
# The following is a hack, whether it works should be checked whenever
# the version is updated from 2.1.0b1
perl -p -i -e "s|CXXFLAGS \+\=|CXXFLAGS += -fPIC|" Makefile
make
make install

%install
# Take everything including sources, makefiles, documentation and examples (only 16MB).
gtar -cv ./| gtar -x -C %i
