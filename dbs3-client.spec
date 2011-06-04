### RPM cms dbs3-client 3.0.10
## INITENV +PATH PYTHONPATH %i/lib/python`echo $PYTHON_VERSION | cut -d. -f 1,2`/site-packages
## INITENV SET DBS3_CLIENT_ROOT %i/
## INITENV SET DBS_READER_URL http://vocms09.cern.ch:8585/dbs/DBSReader 
## INITENV SET DBS_WRITER_URL http://vocms09.cern.ch:8585/dbs/DBSWriter
## INITENV ALIAS dbs python $DBS3_CLIENT_ROOT/bin/dbs.py
%define cvstag %(echo %{realversion} | sed 's/[.]/_/g; s/^/DBS_/')
%define svnserver svn://svn.cern.ch/reps/CMSDMWM
Source0: %svnserver/DBS/tags/%cvstag?scheme=svn+ssh&strategy=export&module=DBS3&output=/%{n}.tar.gz
Requires: python py2-cjson 

%prep
%setup -D -T -b 0 -n DBS3

%build
#cd ../DBS3
python setup.py build_system -s Client
%install
#cd ../DBS3
python setup.py install_system -s Client --prefix=%i
find %i -name '*.egg-info' -exec rm {} \;

# Generate dependencies-setup.{sh,csh} so init.{sh,csh} picks full environment.
mkdir -p %i/etc/profile.d
: > %i/etc/profile.d/dependencies-setup.sh
: > %i/etc/profile.d/dependencies-setup.csh
for tool in $(echo %{requiredtools} | sed -e's|\s+| |;s|^\s+||'); do
  root=$(echo $tool | tr a-z- A-Z_)_ROOT; eval r=\$$root
  if [ X"$r" != X ] && [ -r "$r/etc/profile.d/init.sh" ]; then
    echo "test X\$$root != X || . $r/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
    echo "test X\$$root != X || source $r/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
  fi
done

%post
%{relocateConfig}etc/profile.d/dependencies-setup.*sh

%files
%i/
