### RPM cms das-client 1.8.1
## INITENV +PATH PYTHONPATH %i/bin/
## NOCOMPILER

Source0: https://raw.github.com/dmwm/DAS/1.8.1/src/python/DAS/tools/das_client.py

Requires: python

%prep

%build

%install
mkdir -p %i/bin
cp %SOURCE0 %i/bin
chmod 0755 %i/bin/das_client.py
