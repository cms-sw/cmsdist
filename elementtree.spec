### RPM external elementtree 1.1-XXXX
Source: http://effbot.org/downloads/%n-%realversion-20030511.zip
Requires: python

%prep
%setup -n %n-%realversion-20030511

%build
%install
python setup.py install --prefix=%i/share
