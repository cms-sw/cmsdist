### RPM external oracle 10.1.0.3
Source: http://eulisse.web.cern.ch/eulisse/%n-%v.tgz

%prep
%setup -n %{n}-%{v}
%build
%install
ls
cp -r bin %i
cp -r include %i
cp -r lib %i
