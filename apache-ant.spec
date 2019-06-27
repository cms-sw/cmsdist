### RPM external apache-ant 1.7.0
## INITENV SET ANT_HOME %{i}
Requires: java-jdk python
Source: http://apache.ziply.com/ant/binaries/%{n}-%{realversion}-bin.tar.gz

%prep
%setup -n %{n}-%{realversion}

# replace python calls throuhout the sources
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find . -name "*.py")
%build
%install
tar -cf - . | tar -C %i -xvvf -
# bla bla
