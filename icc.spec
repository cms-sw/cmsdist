### RPM external icc 10.0.023
Source: http://registrationcenter-download.intel.com/irc_nas/728/l_cc_p_%realversion.tar.gz
Source1: http://registrationcenter-download.intel.com/irc_nas/732/l_fc_p_%realversion.tar.gz
%define licenseCpp NB96-HNL7J7JP
%define licenseF95 NDXX-5GNBFFJH

%prep
%setup -n l_cc_p_%realversion
%build
# Actually a binary package. No building required.
%install
cd %i
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icc100023-10.0.023-1.i386.rpm | cpio  -idu 
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icc_ide100023-10.0.023-1.i386.rpm | cpio  -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icce100023-10.0.023-1.em64t.rpm | cpio  -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-idb_ide100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-iidb100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-iidbe100023-10.0.023-1.em64t.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-isubh100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-isubhe100023-10.0.023-1.em64t.rpm | cpio -idu

cp -r %i/opt/intel/cc/%realversion/* %i
cp -r %i/opt/intel/idb/%realversion/* %i

perl -p -i -e "s|<INSTALLDIR>|%i|g" %i/bin/icc \
                                    %i/bin/iccvars.csh \
                                    %i/bin/iccvars.sh \
                                    %i/bin/icpc
rm -rf %i/opt
%post
%{relocateConfig}opt/intel/cc/%realversion/bin/icc
%{relocateConfig}opt/intel/cc/%realversion/bin/iccvars.csh
%{relocateConfig}opt/intel/cc/%realversion/bin/iccvars.sh
%{relocateConfig}opt/intel/cc/%realversion/bin/icpc
