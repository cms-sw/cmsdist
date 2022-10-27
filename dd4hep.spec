## INCLUDE dd4hep-common
### RPM external dd4hep %{dd4hep_version}

%prep
%setup -n %{n}-%{realversion}

%build
export BOOST_ROOT

#Build normal Shared D4Hep without Geant4
rm -rf ../build; mkdir ../build; cd ../build
cmake %{CMAKE_ARGS} -DBUILD_SHARED_LIBS=ON ../%{n}-%{realversion}
make %{makeprocesses} VERBOSE=1
make install

%install

%post
%{relocateConfig}bin/*.sh
