### RPM external cvs2git 5419
Source: http://davidlt.web.cern.ch/davidlt/vault/%{n}-%{realversion}.tar.bz2
Requires: python

%prep
%setup -n %{n}-%{realversion}

%build
./setup.py build

%install
mkdir -p %{i}
mv build/lib %{i}/lib
mv build/script* %{i}/bin
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -l -r -e "#\!.*python" %{i}/bin`
# bla bla
