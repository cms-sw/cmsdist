### RPM external oracle 10.2.0.1
# 10.1.0.3
Source: afs:///afs/cern.ch/sw/lcg/external/oracle/%{v}/%{cmsplatf}?export=/%{n}-%{v}-%{cmsplatf}.tar.gz

# tp://eulisse.web.cern.ch/eulisse/%n-%v.tgz

%prep
%setup -n %{n}-%{v}-%{cmsplatf}
%build
%install
ls
cp -r bin %i
cp -r include %i
cp -r lib %i
