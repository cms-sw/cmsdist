### RPM external py2-formencode 0.5.1
Requires: gcc-wrapper
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION | cut -f1,2 -d.)/site-packages
%define distname FormEncode-%v
Source: http://cheeseshop.python.org/packages/source/F/FormEncode/%{distname}.tar.gz
Requires: python
Patch: formencode-patch-setup

%prep
%setup -n %{distname}
%patch0
%build
## IMPORT gcc-wrapper
%install
python ./setup.py install --prefix=%i
