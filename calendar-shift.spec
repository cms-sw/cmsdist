### RPM cms calendar-shift 1

%define modulename Utils
Requires: python py2-pyopenssl py2-pyxml gcaldaemon
Source: svn://svnweb.cern.ch/guest/cmsawstats/Utils?scheme=http&module=%{modulename}&output=/%{n}.tar.gz

%prep
tar xvzf %_sourcedir/%{n}.tar.gz
#%setup -n %{modulename}

%build

%install
cd %_builddir/%{modulename}
cp -p downtimeFeed_cron.py rssParser.py samdb_dict.py ical.py getCICFeed.py getCMS_To_SAM.py getOIM.py osgParser.py %i/

mkdir %i/Monit # where dynamic data will be stored
mkdir %i/conf
sed -e 's:@ICAL_PATH@:%i/Monit:g' gcal-daemon.cfg > %i/conf/gcal-daemon.cfg
cp -p $GCALDAEMON_ROOT/conf/logger-config.cfg %i/conf/

cat > %i/calendar.sh << \EOF_SCRIPT 
#!/bin/sh
#
# This script performs all steps needed by the calendar application. 
# It replaces both Dong's downtimeFeed_cron.sh and Google's sync-now.sh
# (they sadly don't support command line arguments)
#
# This script can be run as (a)cron job.
#
# Author: Diego S. Gomes (diego@cern.ch) 
# Date: 05/Mar/2010

# Setups the environment (replaces old Dong's "setup.sh" script)
source %i/etc/profile.d/init.sh
export APP_DIR=$CALENDAR_SHIFT_ROOT

# Gets SAM and SiteDB data to do site name conversion (I guess..)
python $CALENDAR_SHIFT_ROOT/getCMS_To_SAM.py > $CALENDAR_SHIFT_ROOT/Monit/getCMS_To_SAM.log 2>&1

# Gets downtime feeds from CIC and OIM and formats them together into ICS 
# files that GCalDaemon can understand
python $CALENDAR_SHIFT_ROOT/downtimeFeed_cron.py > $CALENDAR_SHIFT_ROOT/Monit/downtimeFeed_cron.log 2>&1

# Launch the GCalDaemon only once to send the ICS data to google's account
java -Xmx256m -cp $GCALDAEMON_ROOT/lib/commons-codec.jar:$GCALDAEMON_ROOT/lib/commons-lang.jar:$GCALDAEMON_ROOT/lib/commons-logging.jar:$GCALDAEMON_ROOT/lib/gcal-daemon.jar:$GCALDAEMON_ROOT/lib/gdata-calendar.jar:$GCALDAEMON_ROOT/lib/gdata-client.jar:$GCALDAEMON_ROOT/lib/ical4j.jar:$GCALDAEMON_ROOT/lib/logger.jar:$GCALDAEMON_ROOT/lib/commons-collections.jar:$GCALDAEMON_ROOT/lib/commons-io.jar:$GCALDAEMON_ROOT/lib/shared-asn1.jar:$GCALDAEMON_ROOT/lib/shared-ldap.jar:$GCALDAEMON_ROOT/lib/rome.jar:$GCALDAEMON_ROOT/lib/commons-httpclient.jar:$GCALDAEMON_ROOT/lib/jdom.jar:$GCALDAEMON_ROOT/lib/mail.jar:$GCALDAEMON_ROOT/lib/activation.jar org.gcaldaemon.standalone.Main $CALENDAR_SHIFT_ROOT/conf/gcal-daemon.cfg runonce > $CALENDAR_SHIFT_ROOT/Monit/gcaldaemon-sync.log 2>&1

EOF_SCRIPT
chmod +x %i/calendar.sh

# Dependencies environment
rm -rf %i/etc/profile.d
mkdir -p %i/etc/profile.d
for x in %pkgreqs; do
  case $x in /* ) continue ;; esac
  p=%{instroot}/%{cmsplatf}/$(echo $x | sed 's/\([^+]*\)+\(.*\)+\([A-Z0-9].*\)/\1 \2 \3/' | tr ' ' '/')
  echo ". $p/etc/profile.d/init.sh" >> %i/etc/profile.d/dependencies-setup.sh
  echo "source $p/etc/profile.d/init.csh" >> %i/etc/profile.d/dependencies-setup.csh
done

%post
# Relocation for .ics files under gcal config
%{relocateConfig}conf/gcal-daemon.cfg
# Relocation for calendar.sh
%{relocateConfig}calendar.sh
# Relocation for dependencies environment
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

