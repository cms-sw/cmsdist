### RPM external vbfnlo 3.0.0beta5
Source: git+https://github.com/vbfnlo/%{n}.git?obj=master/v%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

BuildRequires: autotools

%prep
%setup -q -n %{n}-%{realversion}

%build
CXX="$(which g++) -std=c++11"
CC="$(which gcc)"
FC="$(which gfortran)"

./configure --prefix=%i \
            --enable-processes=vbf,hjjj \
	    FC=${FC}  FCFLAGS=-std=legacy 

make %{makeprocesses}

%install
make install

%post

