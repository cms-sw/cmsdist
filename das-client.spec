### RPM cms das-client 2.5.0
## INITENV +PATH PYTHONPATH %i/bin/
## NOCOMPILER

Source0: https://raw.github.com/dmwm/DAS/%{realversion}/src/python/DAS/tools/das_client.py

Requires: python

%prep

%build

%install
mkdir -p %{i}/bin
cp %{SOURCE0} %{i}/bin
chmod 0755 %{i}/bin/das_client.py
