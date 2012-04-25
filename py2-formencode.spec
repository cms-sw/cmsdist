### RPM external py2-formencode 0.7.1
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
%define distname FormEncode-%realversion
Source: http://cheeseshop.python.org/packages/source/F/FormEncode/%{distname}.tar.gz
Requires: python
Patch0: formencode-patch-setup
Patch1: formencode

%prep
%setup -n %{distname}
%patch0
%patch1 -p1
%build
%install
python ./setup.py install --prefix=%i
