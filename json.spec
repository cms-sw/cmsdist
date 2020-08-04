### RPM external json 3.7.3
## NOCOMPILER

Source: https://github.com/nlohmann/%{n}/releases/download/v%{realversion}/include.zip

%prep
%setup -c

%build

%install
mkdir -p %{i}/include/nlohmann
cp -a include/nlohmann/json_fwd.hpp     %{i}/include/nlohmann/
cp -a single_include/nlohmann/json.hpp  %{i}/include/nlohmann/

%post
