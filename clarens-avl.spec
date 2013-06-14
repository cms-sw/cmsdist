### RPM external clarens-avl 0.3.4
%define pythonv %(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib

Summary: An AVL tree implementation for Python

Source0: http://julian.ultralight.org/clarens/devel/%{n}-%{v}.tar.gz
Vendor: Conrad Steenberg <conrad@hep.caltech.edu>
Url:  http://clarens.sourceforge.net
Packager: Conrad Steenberg <conrad@hep.caltech.edu>

Requires: python pyrex

%description
An implementation of serializable balanced AVL trees with Python bindings

%prep
%setup -n %n-%v 

%build
make clean
make

%install
mkdir -p %i/lib
cp avl_string.so avl_double.so %i/lib

mkdir -p %i/doc
cp COPYING README %i/doc
