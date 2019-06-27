### RPM external catch2 2.2.2
Source: https://raw.githubusercontent.com/catchorg/Catch2/v%{realversion}/single_include/catch.hpp

%prep

%build

%install
mkdir %{i}/include
cp %{_sourcedir}/catch.hpp %{i}/include/
# bla bla
