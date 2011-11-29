### RPM cms CmsProjectBuilder 1.33
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
%define svnversion %realversion

Source: svn://svn.cern.ch/reps/CMSIntBld/tags/CmsProjectBuilder/V00-00-01/?scheme=svn+ssh&strategy=export&module=CmsProjectBuilder&output=/CmsProjectBuilder.tar.gz 


Requires: python py2-simplejson py2-sqlalchemy py2-httplib2

%prep
%setup -n CmsProjectBuilder

%build
python setup2.py build

%install
python setup2.py install --prefix=%i


%post

