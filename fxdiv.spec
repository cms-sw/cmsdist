### RPM external fxdiv 2020-04-17

%define commit b408327ac2a15ec3e43352421954f5b1967701d1

Source0: git+https://github.com/Maratyszcza/FXdiv.git?obj=master/%{commit}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %{n}-%{realversion}

%build

%install
mkdir -p %{i}/include
cp -a include/fxdiv.h     %{i}/include/
