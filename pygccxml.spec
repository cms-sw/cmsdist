### RPM external pygccxml 0.8.0
## INITENV +PATH PYTHONPATH %i/lib/python%(echo $PYTHON_VERSION | cut -d. -f 1,2)/site-packages
Source: http://puzzle.dl.sourceforge.net/sourceforge/%n/%n-%v.tar.gz
Requires: python
%build
%install
python setup.py install --prefix=%i
