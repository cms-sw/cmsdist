### RPM external pyqt 4.4.4
## INITENV +PATH PYTHONPATH %i/lib/python2.4/site-packages
## BUILDIF case %cmsplatf in osx*) false;; *) true;; esac
Source: http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-x11-gpl-%realversion.tar.gz
Requires: python
Requires: qt
Requires: sip

%prep
%setup -n PyQt-x11-gpl-%realversion

%build
echo yes | python ./configure.py -b %i/bin -d %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages -e %i/include --no-sip-files --no-designer-plugin
make %makeprocesses

%install
make install


