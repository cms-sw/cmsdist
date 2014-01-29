### RPM external clarens-light 0.1
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages
## INITENV +PATH PATH %{i}/bin

Summary: A Python-only implementation of the Clarens server
Group: Development/Libraries
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/ClarensLight-%v.tar.gz
Requires: python py2-pyopenssl
%prep
%setup -n ClarensLight-%{v}
%build

%install
mkdir -p %{i}/lib/python%{pythonv}/site-packages
mkdir -p %{i}/bin

mv Clarens %{i}/lib/python%{pythonv}/site-packages
mv ClarensLightServer %{i}/bin

