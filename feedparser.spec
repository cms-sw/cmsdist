### RPM external feedparser 4.1
%define pythonv `echo $PYTHON_VERSION |cut -d. -f1,2`
## INITENV +PATH PYTHONPATH %i/lib/python%{pythonv}/site-packages
Source: http://feedparser.googlecode.com/files/feedparser-%realversion.zip
Requires: python

%prep
rm -rf feedparser-%realversion
unzip -d feedparser-%realversion %_sourcedir/feedparser-%realversion.zip
cd feedparser-%realversion
%build
%install
python setup.py install --prefix=%i 
