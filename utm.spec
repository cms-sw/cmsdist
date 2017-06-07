### RPM external utm utm_0.6.5
Source: git+https://gitlab.cern.ch/cms-l1t-utm/utm.git?obj=master/%{realversion}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: gmake
Requires: xerces-c
Requires: boost
Patch0: utm-0.6.4-boost-and-transform-fix

%prep
%setup -n %{n}-%{realversion}
%patch0 -p1

%build
export XERCES_C_BASE=${XERCES_C_ROOT}
export BOOST_BASE=${BOOST_ROOT}
make %{makeprocesses} -f Makefile.standalone all
make %{makeprocesses} -f Makefile.standalone install

%install
cp -r lib %{i}/lib
cp -r include %{i}/include
cp -r xsd-type %{i}/xsd-type
cp -r menu.xsd %{i}/menu.xsd


