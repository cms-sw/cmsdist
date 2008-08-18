### RPM external srmcp 1.8.0-15p8
## INITENV +PATH PATH %i/bin:%i/sbin
## INITENV SET SRM_PATH %i

Source: http://www.dcache.org/downloads/1.8.0/dcache-srmclient-%realversion.noarch.rpm
Requires:  java-jdk

%prep
rpm2cpio %{_sourcedir}/dcache-srmclient-%realversion.noarch.rpm | cpio -ivd 

%build

%install
mv %{_builddir}/opt/d-cache/srm/* %i

# unset SRM_PATH SRM_CONFIG || true
# # (cd .. && tar -cf - srmclient) | (cd %i && tar -xf -)
# mkdir -p %i/etc
# SRM_PATH=%i SRM_CONFIG=%i/etc/config.xml \
# %i/sbin/srm \
# -x509_user_trusted_certificates /etc/grid-security/certificates \
# -copy file:////dev/null file:////dev/null > /dev/null 2>&1 || true

# perl -p -i -e "s|$HOME|%i|" %i/etc/config.xml

# Build dependencies-setup

mkdir -p %{i}/etc/profile.d
 
(echo "#!/bin/sh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.sh"; \
) > %{i}/etc/profile.d/dependencies-setup.sh
                                                                                                     
(echo "#!/bin/tcsh"; \
 echo "source $JAVA_JDK_ROOT/etc/profile.d/init.csh"; \
) > %{i}/etc/profile.d/dependencies-setup.csh
                                                                                                     
%post
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh

