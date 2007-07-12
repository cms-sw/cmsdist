### RPM external apt 0.5.15lorg3.2-CMS3
## INITENV SET APT_CONFIG %{i}/etc/apt.conf

Source:  http://apt-rpm.org/releases/%n-%realversion.tar.bz2
Source1: bootstrap
Source2: cms-apt-migration
Requires: libxml2 beecrypt rpm zlib bz2lib openssl
Patch0: apt-rpm449
Patch1: apt-rpm446
Patch2: apt

%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64
%else
%define libdir lib
%endif


%prep
%setup -n %n-%{realversion}
case $RPM_VERSION in
    4.4.9*)
%patch0 -p0
        ;;
    4.4.6*)
%patch1 -p0
        ;;
esac

# scandir has a different prototype between macosx and linux.
%if "%(uname)" == "Darwin"
%patch2 -p1
%endif

%build
export CFLAGS="-O0 -g"
export CXXFLAGS="-O0 -g"
export CPPFLAGS="-I$BZ2LIB_ROOT/include -I$BEECRYPT_ROOT/include -I$RPM_ROOT/include -I$RPM_ROOT/include/rpm"
export LDFLAGS="-L$BZ2LIB_ROOT/lib -L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"
export LIBDIR="$LIBS"
export LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2 -I$BEECRYPT_ROOT/include -I$RPM_ROOT/include"
export LIBXML2_LIBS="-lxml2 -L$LIBXML2_ROOT/lib -L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"

./configure --prefix=%{i} --exec-prefix=%{i} \
                            --disable-nls \
                            --disable-dependency-tracking \
                            --without-libintl-prefix \
                            --disable-docs \
                            --disable-rpath
make %makeprocesses


%install
make install
mkdir -p %{i}/etc/profile.d
(echo "#!/bin/sh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.sh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.sh" ) > %{i}/etc/profile.d/dependencies-setup.sh
(echo "#!/bin/tcsh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.csh"; \
 echo "source $LIBXML2_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh


mkdir -p %{i}/etc/apt
cat << \EOF_APT_CONF > %{i}/etc/apt.conf
Dir "%{instroot}"
{
  // Location of the state dir
    State "%{cmsplatf}/var/lib/apt/"
      {
           lists "lists/";
           xstatus "xstatus";
           userstatus "status.user";
           status "var/lib/dpkg/status";
           cdroms "cdroms.list";
      };

  // Location of the cache dir
    Cache "%{cmsplatf}/var/lib/cache" {
                               archives "%{cmsplatf}";
                               srcpkgcache "srcpkgcache.bin";
                               pkgcache "pkgcache.bin";
                           };

  // Locations of binaries
      Bin {
             methods "%{i}/lib/apt/methods/";
             gzip "/bin/gzip";
             dpkg "/usr/bin/dpkg";
             dpkg-source "/usr/bin/dpkg-source";
             dpkg-buildpackage "/usr/bin/dpkg-buildpackage";
             apt-get "%{i}/bin/apt-get-wrapper";
             apt-cache "%{i}/bin/apt-cache-wrapper";
             rpm "%{i}/bin/rpm-wrapper";
        };
                                                                                                          

  // Config files
    Etc "%{cmsplatf}/external/apt/%{v}/etc/" {
                       sourcelist "sources.list";
                       main "apt.conf";
                       preferences "preferences";
                   };
};

Debug::pkgProblemResolver="1";

RPM
{
    PM "external";
    Options { };
    Install-Options { "--force";"--prefix";"%{instroot}";"--ignoreos";"--ignorearch";};
    RootDir "%{instroot}";
    Architecture "%{cmsplatf}";
};
EOF_APT_CONF


cat << \EOF_SOURCES_LIST > %{i}/etc/sources.list
rpm http://cmsrep.cern.ch cms/cpt/Software/download/cms/apt/%{cmsplatf} cms lcg external
rpm-src http://cmsrep.cern.ch cms/cpt/Software/download/cms/apt/%{cmsplatf} cms lcg external
# This are defined to support experimental repositories. The bootstrap file rewrites and uncomments
# them when passed the appropriate commandline option. 
## rpm @SERVER@ @SERVER_PATH@/@REPOSITORY@/apt/%{cmsplatf} @GROUPS@  
## rpm-src @SERVER@ @SERVER_PATH@/@REPOSITORY@/apt/%{cmsplatf} @GROUPS@
EOF_SOURCES_LIST

cat << \EOF_RPMPRIORITIES > %{i}/etc/rpmpriorities
Essantial:

EOF_RPMPRIORITIES

cat << \EOF_BIN_APT_CACHE_WRAPPER > %{i}/bin/apt-cache-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-cache $@
EOF_BIN_APT_CACHE_WRAPPER
chmod +x %{i}/bin/apt-cache-wrapper

cat << \EOF_BIN_APT_GET_WRAPPER > %{i}/bin/apt-get-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-get $@
EOF_BIN_APT_GET_WRAPPER
chmod +x %{i}/bin/apt-get-wrapper

cat << \EOF_BIN_RPM > %{i}/bin/rpm-wrapper
#!/bin/sh
if [ X"$(id -u)" = X0 ]; then
  echo "*** CMS SOFTWARE INSTALLATION ABORTED ***" 1>&2
  echo "CMS software cannot be installed as the super-user." 1>&2
  echo "(We recommend reading any standard unix security guide.)" 1>&2
  exit 1
fi
touch %{instroot}/log.txt
echo rpm ${1+"$@"} >> %{instroot}/log.txt
exec rpm ${1+"$@"}
EOF_BIN_RPM
chmod +x %{i}/bin/rpm-wrapper

cat %_sourcedir/bootstrap | perl -p -e "s!\@CMSPLATF\@!%{cmsplatf}!g;
                                        s!\@GCC_VERSION\@!$GCC_VERSION!g;
                                        s!\@RPM_VERSION\@!$RPM_VERSION!g;
                                        s!\@DB4_VERSION\@!$DB4_VERSION!g;
                                        s!\@LIBXML2_VERSION\@!$LIBXML2_VERSION!g;
                                        s!\@OPENSSL_VERSION\@!$OPENSSL_VERSION!g;
                                        s!\@BEECRYPT_VERSION\@!$BEECRYPT_VERSION!g;
                                        s!\@BZ2LIB_VERSION\@!$BZ2LIB_VERSION!g;
                                        s!\@ZLIB_VERSION\@!$ZLIB_VERSION!g;
                                        s!\@EXPAT_VERSION\@!$EXPAT_VERSION!g;
                                        s!\@ELFUTILS_VERSION\@!$ELFUTILS_VERSION!g;
                                        s!\@NEON_VERSION\@!$NEON_VERSION!g;
                                        s!\@GCC_REVISION\@!$GCC_REVISION!g;
                                        s!\@BEECRYPT_REVISION\@!$BEECRYPT_REVISION!g;
                                        s!\@RPM_REVISION\@!$RPM_REVISION!g;
                                        s!\@OPENSSL_REVISION\@!$OPENSSL_REVISION!g;
                                        s!\@DB4_REVISION\@!$DB4_REVISION!g;
                                        s!\@LIBXML2_REVISION\@!$LIBXML2_REVISION!g;
                                        s!\@BZ2LIB_REVISION\@!$BZ2LIB_REVISION!g;
                                        s!\@ZLIB_REVISION\@!$ZLIB_REVISION!g;
                                        s!\@EXPAT_REVISION\@!$EXPAT_REVISION!g;
                                        s!\@NEON_REVISION\@!$NEON_REVISION!g;
                                        s!\@ELFUTILS_REVISION\@!$ELFUTILS_REVISION!g;
                                        s!\@APT_VERSION\@!%{v}!g;
                                        s!\@APT_REVISION\@!%{pkgrevision}!g;
                                        s!\@INSTROOT\@!%{instroot}!g;
                                        " > %{i}/bin/bootstrap-%{cmsplatf}.sh

cat %_sourcedir/cms-apt-migration | perl -p -e "s!\@CMSPLATF\@!%{cmsplatf}!g;
                                        s!\@GCC_VERSION\@!$GCC_VERSION!g;
                                        s!\@RPM_VERSION\@!$RPM_VERSION!g;
                                        s!\@DB4_VERSION\@!$DB4_VERSION!g;
                                        s!\@LIBXML2_VERSION\@!$LIBXML2_VERSION!g;
                                        s!\@OPENSSL_VERSION\@!$OPENSSL_VERSION!g;
                                        s!\@BEECRYPT_VERSION\@!$BEECRYPT_VERSION!g;
                                        s!\@BZ2LIB_VERSION\@!$BZ2LIB_VERSION!g;
                                        s!\@ZLIB_VERSION\@!$ZLIB_VERSION!g;
                                        s!\@EXPAT_VERSION\@!$EXPAT_VERSION!g;
                                        s!\@ELFUTILS_VERSION\@!$ELFUTILS_VERSION!g;
                                        s!\@NEON_VERSION\@!$NEON_VERSION!g;
                                        s!\@GCC_REVISION\@!$GCC_REVISION!g;
                                        s!\@BEECRYPT_REVISION\@!$BEECRYPT_REVISION!g;
                                        s!\@RPM_REVISION\@!$RPM_REVISION!g;
                                        s!\@OPENSSL_REVISION\@!$OPENSSL_REVISION!g;
                                        s!\@DB4_REVISION\@!$DB4_REVISION!g;
                                        s!\@LIBXML2_REVISION\@!$LIBXML2_REVISION!g;
                                        s!\@BZ2LIB_REVISION\@!$BZ2LIB_REVISION!g;
                                        s!\@ZLIB_REVISION\@!$ZLIB_REVISION!g;
                                        s!\@EXPAT_REVISION\@!$EXPAT_REVISION!g;
                                        s!\@NEON_REVISION\@!$NEON_REVISION!g;
                                        s!\@ELFUTILS_REVISION\@!$ELFUTILS_REVISION!g;
                                        s!\@APT_VERSION\@!%{v}!g;
                                        s!\@APT_REVISION\@!%{pkgrevision}!g;
                                        s!\@INSTROOT\@!%{instroot}!g;" > %{i}/bin/cms-apt-migration-%{cmsplatf}.sh

%post
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/apt/lists/partial
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/rpm 
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/cache/%{cmsplatf}/partial
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/rpm
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/lib/apt/methods
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/dpkg/status
mkdir -p $RPM_INSTALL_PREFIX/bin
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/cache/%{cmsplatf}
%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
%{relocateConfig}bin/apt-cache-wrapper
%{relocateConfig}bin/apt-get-wrapper
%{relocateConfig}bin/rpm-wrapper
%{relocateConfig}etc/apt.conf 
