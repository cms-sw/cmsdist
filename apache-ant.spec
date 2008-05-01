### RPM external apache-ant 1.7.0
## INITENV SET ANT_HOME %{i}
Requires: java-jdk python
Source: http://apache.ziply.com/ant/binaries/%{n}-%{v}-bin.tar.gz

%prep
%setup -n %{n}-%{v}

# replace python calls throuhout the sources
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find .)
%build
%install
tar -cf - . | tar -C %i -xvvf -
