### RPM external elementtree 1.2.6
Source: http://effbot.org/downloads/%n-%realversion-20050316.zip
Requires: python
 
%prep
%setup -n %n-%realversion-20050316

%build
%install
python setup.py install --prefix=%i/share
