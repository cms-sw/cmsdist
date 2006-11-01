### RPM external py2-cheetah 2.0rc7
%define pythonv %(echo $PYTHON_VERSION |cut -d. -f1,2)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/cheetahtemplate/Cheetah-%v.tar.gz
Requires: python

%prep
%setup -n Cheetah-%v
%build
%install
python setup.py install --prefix=%i
