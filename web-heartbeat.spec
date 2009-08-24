### RPM cms web-heartbeat forHEARTBEATr01

# The following tar.gz file will be generated automatically by the CVS server some
# minutes after commiting the files
Source0: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&strategy=export&nocache=true&module=COMP/SITECONF/T1_CH_CERN/Heartbeat&export=conf&tag=-r%{v}&output=/%{n}.tar.gz

Requires: wmcore 

%prep
# -T: Disable the automatic unpacking of the archives
# -b 0: only unpack the source directive of the given number, such as –b 0 for source0:, before changing to the directory
# -n conf: name the directory as conf
%setup -T -b 0 -n conf

%build
# It is a script. Nothing to build.

%install
# Copy files files to the destine installation directory.
cp -p %_builddir/conf/* %i/
#touch %instroot/apache2/logs/start_stop.log

%post
echo "install prefix in post section: $RPM_INSTALL_PREFIX"
# should configure the cronjob here?

%files
%i/
