### RPM external py3-pydoop 2.0.0
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}

Source0: https://pypi.python.org/packages/source/p/pydoop/pydoop-%realversion.tar.gz
Source1: http://www-eu.apache.org/dist/hadoop/common/hadoop-2.6.4/hadoop-2.6.4.tar.gz 
Requires: zlib bz2lib openssl python3 py3-setuptools py3-avro
BuildRequires: java-jdk
Provides: libjvm.so()(64bit)

%prep
%setup -T -b 1 -n hadoop-2.6.4
%setup -n pydoop-%realversion

%build
export JAVA_HOME=${JAVA_JDK_ROOT}
export GCC_ROOT
export PYTHON_ROOT
export HADOOP_HOME=%{_builddir}/hadoop-2.6.4
python3 setup.py build

%install
export JAVA_HOME=${JAVA_JDK_ROOT}
export GCC_ROOT
export PYTHON_ROOT
export HADOOP_HOME=%{_builddir}/hadoop-2.6.4
python3 setup.py install --prefix=%i --single-version-externally-managed --record=/dev/null
find %i -name '*.egg-info' -exec rm {} \;
# use /usr/bin/env python
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
