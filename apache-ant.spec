
### RPM external apache-ant 1.6.5
Requires: java-jdk python
Source: http://apache.ziply.com/ant/binaries/%{n}-%{v}-bin.tar.gz

%prep
echo "PWD in prep is:" `pwd`
%setup -n %{n}-%{v}

# replace python calls throuhout the sources
perl -p -i -e "s|#!/usr/bin/python|#!/usr/bin/env python|" $(find .)

%build
echo "PWD in build is:" `pwd`
%install
echo "PWD in install is:" `pwd`

tar -cf - . | tar -C %i -xvvf -
