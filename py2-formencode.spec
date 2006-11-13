### RPM external formencode 0.4
%define distname FormEncode-%v
Source: http://cheeseshop.python.org/packages/source/F/FormEncode/%{distname}.tar.gz
Requires: python

%prep
%setup %{distname}
%build
%install
python ./setup.py --prefix=%i
