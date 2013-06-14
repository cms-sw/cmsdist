### RPM external jobmon_client 0.1
%define pythonv $(echo $PYTHON_VERSION | cut -d. -f 1,2)
## INITENV +PATH PYTHONPATH %{i}/lib/python%{pythonv}/site-packages

Summary: A Client to connect to the JobMon service
Group: Development/Libraries
Vendor: JobMon Developers
Url: http://jobmon.sourceforge.net
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/%n-%v.tar.gz

%prep
%setup -n %n

%build

%install
set
mkdir -p %{i}/lib/python%{pythonv}/site-packages
cp ClarensDpe.py  JobMonDaemon.py  JobMon.py  Usage.html \
  %{i}/lib/python%{pythonv}/site-packages

