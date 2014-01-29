### RPM cms xcmsi-compatibility 1.0
# This spec is used to link the old scramdb to the new one.
Source: none
Requires: SCRAM SCRAMV1 cms-env

%prep
%build
%install

%post
echo "Linking old XCMSI scram database to the new one..."
if [ ! -f $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup ]
then
    echo "XCMSI installation not found. Quitting without doing anything."
else
    source $RPM_INSTALL_PREFIX/cmsset_default.sh
    scramv1 db -link $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup
    scramv0 db link $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup
fi

%preun
echo "Unlinking old XCMSI scram database from the new one..."
if [ ! -f $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup ]
then 
    echo "XCMSI installation not found. Quitting without doing anything."
    exit 0
else
    source $RPM_INSTALL_PREFIX/cmsset_default.sh
    scramv1 db -unlink $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup
    scramv0 db unlink $RPM_INSTALL_PREFIX/Releases/SCRAM/scramdb/project.lookup
fi
