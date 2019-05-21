### RPM external hjets 1.2
Source: https://hjets.hepforge.org/downloads/HJets-%{realversion}.tar.gz

Requires: herwigpp

 
BuildRequires: autotools

%prep
%setup -n HJets-%{realversion}

%build
CXX="$(which g++) -fPIC"
CC="$(which gcc) -fPIC"
FC="$(which gfortran) -fPIC" 

./configure --prefix=%i --with-herwig=${HERWIGPP_ROOT}

make %makeprocesses

%install
make install

%post

