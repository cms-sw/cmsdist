### RPM external icc 10.0.023
Source: http://registrationcenter-download.intel.com/irc_nas/728/l_cc_p_%realversion.tar.gz
Source1: http://registrationcenter-download.intel.com/irc_nas/732/l_fc_p_%realversion.tar.gz
%define licenseCpp NB96-HNL7J7JP
%define licenseF95 NDXX-5GNBFFJH

%prep
%setup -T -b 0 -n l_cc_p_%realversion 
%setup -D -T -b 1 -n l_fc_p_%realversion
%build
# Actually a binary package. No building required.
%install
cd %i
%define cpu %(echo %cmsplatf | cut -f2 -d_)

%define arch_postfix %{nil}
%if "%cpu" == "ia32"
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icc100023-10.0.023-1.i386.rpm | cpio  -idu 
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-iidb100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-isubh100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_fc_p_10.0.023/data/intel-ifort100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_fc_p_10.0.023/data/intel-iidb100023-10.0.023-1.i386.rpm | cpio -idu
%endif

%if "%cpu" == "amd64"
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-iidbe100023-10.0.023-1.em64t.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icc_ide100023-10.0.023-1.i386.rpm | cpio  -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-icce100023-10.0.023-1.em64t.rpm | cpio  -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-idb_ide100023-10.0.023-1.i386.rpm | cpio -idu
rpm2cpio %_builddir/l_cc_p_%realversion/data/intel-isubhe100023-10.0.023-1.em64t.rpm | cpio -idu
rpm2cpio %_builddir/l_fc_p_10.0.023/data/intel-iforte100023-10.0.023-1.em64t.rpm | cpio -idu
rpm2cpio %_builddir/l_fc_p_10.0.023/data/intel-iidbe100023-10.0.023-1.em64t.rpm | cpio -idu
%define arch_postfix e
%endif

cp -r %i/opt/intel/cc%{arch_postfix}/%realversion/* %i
cp -r %i/opt/intel/idb%{arch_postfix}/%realversion/* %i
cp -r %i/opt/intel/fc%{arch_postfix}/%realversion/* %i 

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
