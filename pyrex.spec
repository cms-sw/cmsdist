### RPM external pyrex 0.9.3.1
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages
## INITENV +PATH PATH %{i}/bin

Summary: A language for writing Python extension modules.
Group: Development/Libraries
Vendor: Greg Ewing <greg@cosc.canterbury.ac.nz>
Url: http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/Pyrex-%{v}.tar.gz
Requires: python 
%prep
%setup -n Pyrex-%{v}
%build
python setup.py build 
%install
python setup.py install --prefix=%i
