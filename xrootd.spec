### RPM external xrootd 20070321-1251p1
Source: http://xrootd.slac.stanford.edu/download/%v/%n-%v.src.tgz
#

%prep 
%setup -n xrootd

%build
./configure.classic
gmake

%install
mkdir %i/bin
mkdir %i/lib
mkdir %i/etc
mkdir %i/utils
cp -r bin/arch/* %i/bin
cp -r lib/arch/* %i/lib
cp -r utils/* %i/utils
cp -r etc/* %i/etc
rm -fR %i/bin/CVS %i/lib/CVS %i/utils/CVS %i/etc/CVS
# Need to fix the following in the xrootd CVS
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/etc/XrdOlbMonPerf
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_PreStage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_MigrPurg
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/fs_stat
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_MonP.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_Lock.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_prep
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Stage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_name2name.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_CAlloc.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Xeq
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/XrdOlbNotify.pm

%post

