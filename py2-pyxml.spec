### RPM external py2-pyxml 0.8.4
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://switch.dl.sourceforge.net/sourceforge/pyxml/PyXML-%{v}.tar.gz
Requires: python expat

%prep
%setup -n PyXML-%{v}
%build
./setup.py build
%install
./setup.py install --prefix=%{i}
