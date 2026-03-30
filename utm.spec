### RPM external utm utm_0.14.1
Source: git+https://gitlab.cern.ch/cms-l1t-utm/utm.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Patch0: utm-boost190
BuildRequires: gmake
Requires: xerces-c boost

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
export XERCES_C_BASE=${XERCES_C_ROOT}
export BOOST_BASE=${BOOST_ROOT}
./configure
make %{makeprocesses} all

%install
make %{makeprocesses} install
cp -r lib %{i}/lib
cp -r include %{i}/include
cp -r xsd-type %{i}/xsd-type
cp -r menu.xsd %{i}/menu.xsd


