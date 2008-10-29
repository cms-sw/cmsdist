### RPM external py2-pysqlite 2.4.0
%define pythonv %(echo $PYTHON_VERSION | cut -f1,2 -d.)
%define distname pysqlite-%realversion
%define distmaindir %(echo %realversion | cut -d. -f1,2)
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -f1,2 -d.`/site-packages
Source: http://cmsrep.cern.ch/cmssw/pysqlite-mirror/%{distname}.tar.gz
Requires: python sqlite

%prep
%setup -n %{distname}
%build
perl -p -i -e "s!include_dirs=.*!include_dirs=$SQLITE_ROOT/include!" setup.cfg
perl -p -i -e "s!library_dirs=.*!library_dirs=$SQLITE_ROOT/lib!" setup.cfg
python setup.py build
%install
python setup.py install --prefix=%i
