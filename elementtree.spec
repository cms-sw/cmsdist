### RPM external elementtree 1.1
Source: http://effbot.org/downloads/%n-%v-20030511.zip
Requires: python

%prep
%setup -n %n-%v-20030511

%build
%install
python setup.py install --prefix=%i
