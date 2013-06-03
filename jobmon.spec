### RPM external jobmon 0.1

Summary: A Clarens service for interactive job communication
Group: Development/Libraries
Vendor: JobMon Developers
Url: http://jobmon.sourceforge.net
Packager: Conrad Steenberg <conrad@hep.caltech.edu>
Source: http://julian.ultralight.org/clarens/devel/%n-%v.tar.gz

%build

%install
set
mkdir -p %i/service
cp .clarens_access JobMonTcpServer.py JobMonUtil.py __init__.py\
 %i/service

mkdir -p %i/config
cp config %i/config

mkdir -p %i/etc/profile.d

cat << DEPS_SETUP > %i/etc/profile.d/dependencies-setup.sh
#!/bin/sh
if [ ! -f \$CLARENS_SERVER_ROOT/conf/default/jobmon/config]; then
  ln -sf \$JOBMON_ROOT/config \$CLARENS_SERVER_ROOT/conf/default/jobmon
fi


DEPS_SETUP

