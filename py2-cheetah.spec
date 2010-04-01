### RPM external py2-cheetah 2.0rc8
Requires: python
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
Source: http://switch.dl.sourceforge.net/sourceforge/cheetahtemplate/Cheetah-%realversion.tar.gz

%prep
%setup -n Cheetah-%realversion
%build
%install
python setup.py install --prefix=%i
perl -p -i -e "s|#\!.*python|#!/usr/bin/env python|" %i/bin/cheetah
perl -p -i -e "s|#\!.*python|#!/usr/bin/env python|" %i/bin/cheetah-compile
