### RPM external histogrammar 1.0.3
## INITENV +PATH PYTHONPATH %i/$PYTHON_LIB_SITE_PACKAGES
Source: https://pypi.python.org/packages/68/d5/a3b095f9513643832f8b767a1c1739c78751753e880317cbbe3488d69323/histogrammar-%{realversion}.tar.gz
Requires: python
Requires: py2-numpy
Requires: py2-pandas
Requires: root

%prep
%setup -n histogrammar-%{realversion}

%build
%install

mkdir -p %{i}/$PYTHON_LIB_SITE_PACKAGES
export PYTHONPATH=%{i}/$PYTHON_LIB_SITE_PACKAGES:${PYTHONPATH}

python setup.py build
python setup.py install --prefix=%{i}
#find %{i} -name '*.egg-info' -exec rm {} \;
perl -p -i -e "s|^#!.*python(.*)|#!/usr/bin/env python$1|" `grep -r -e "^#\!.*python.*" %i | cut -d: -f1`
