### RPM external py2-json 0.1
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}

Summary: Javascript Object Notation implementation for Python
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/python-json-%v.tar.gz
URL: http://json-rpc.org/pyjsonrpc/index.xhtml
Requires: python 
%prep
%setup -n python-json-%{v}

%build

%install
mkdir -p %{i}/lib/python%{pythonv}

cp json.py jsonrpc.py %{i}/lib/python%{pythonv}

