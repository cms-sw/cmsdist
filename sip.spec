### RPM external sip 4.11.2
## INITENV +PATH PYTHONPATH %i/lib/python$(echo $PYTHON_VERSION |cut -d. -f 1,2)/site-packages
#Source: http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-%realversion.tar.gz
Source: http://cmsrep.cern.ch/cmssw/pyqt-mirror/sip-%realversion.tar.gz
Patch0: sip-4.11.1-macosx
Requires: python
%prep
%setup -n sip-%realversion 
%patch0 -p1

%build
python ./configure.py -v %i/share -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages -e %i/include
make %makeprocesses

%install
make install

%post
%{relocateConfig}lib/python2.7/site-packages/sipconfig.py
