### RPM external py2-yaml 3.09
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages

Source: http://pyyaml.org/download/pyyaml/PyYAML-%realversion.tar.gz
Requires: python libyaml py2-pyrex

%prep
%setup -n PyYAML-%realversion
cat >> setup.cfg <<-EOF
	[build_ext]
	include_dirs = $LIBYAML_ROOT/include
	library_dirs = $LIBYAML_ROOT/lib
EOF

%build
python setup.py build

%install
python setup.py --with-libyaml install --prefix=%i
egrep -r -l '^#!.*python' %i | xargs perl -p -i -e 's{^#!.*python.*}{#!/usr/bin/env python}'
find %i -name '*.egg-info' -exec rm {} \;
