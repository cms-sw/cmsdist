### RPM external castor 2.1.0-0
%define downloadv %(echo %v | cut -d- -f1)

Source: http://cern.ch/castor/DIST/CERN/savannah/CASTOR.pkg/%v/castor-%downloadv.tar.gz

%prep
%setup -n castor-%downloadv