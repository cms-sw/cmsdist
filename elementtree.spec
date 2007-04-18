### RPM external elementtree 1.1
Requires: gcc-wrapper
Source: http://effbot.org/downloads/%n-%v-20030511.zip
Requires: python

%prep
%setup -n %n-%v-20030511

%build
## IMPORT gcc-wrapper
%install
python setup.py install --prefix=%i/share
