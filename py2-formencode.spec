### RPM external py2-formencode 0.7.1
## INITENV +PATH PYTHONPATH %i/${PYTHON_LIB_SITE_PACKAGES}
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
python setup.py build

%install
python setup.py install --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;
