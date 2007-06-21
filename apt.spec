### RPM external apt 0.5.15lorg3.2-wt1
## INITENV SET APT_CONFIG %{i}/etc/apt/apt.conf

Source:  http://apt-rpm.org/releases/%n-%realversion.tar.bz2
Source1: bootstrap
Patch0: apt-rpm449
Requires: libxml2 beecrypt rpm zlib bz2lib openssl
%if "%(echo %{cmsos} | cut -d_ -f 2 | sed -e 's|.*64.*|64|')" == "64"
%define libdir lib64
%else
%define libdir lib
%endif

%prep
%setup -n %n-%{realversion}
%patch0 -p0
%build
export CPPFLAGS="-I$BEECRYPT_ROOT/include -I$RPM_ROOT/include -I$RPM_ROOT/include/rpm"
export LDFLAGS="-L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"
export LIBDIR="$LIBS"
export LIBXML2_CFLAGS="-I$LIBXML2_ROOT/include/libxml2 -I$BEECRYPT_ROOT/include -I$RPM_ROOT/include"
export LIBXML2_LIBS="-lxml2 -L$LIBXML2_ROOT/lib -L$BEECRYPT_ROOT/%{libdir} -L$RPM_ROOT/%{libdir}"

./configure --prefix=%{i} --exec-prefix=%{i} \
                            --disable-nls \
                            --disable-dependency-tracking \
                            --without-libintl-prefix \
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
cat << \EOF_APT_CONF > %{i}/etc/apt/apt.conf
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
             methods "%{i}%{libdir}/apt/methods/";
             gzip "/bin/gzip";
             dpkg "/usr/bin/dpkg";
             dpkg-source "/usr/bin/dpkg-source";
             dpkg-buildpackage "/usr/bin/dpkg-buildpackage";
             apt-get "%{instroot}/bin/apt-get-wrapper";
             apt-cache "%{instroot}/bin/apt-cache-wrapper";
             rpm "%{instroot}/bin/rpm-wrapper";
        };
                                                                                                          

  // Config files
    Etc "%{cmsplatf}/etc/apt/" {
                       sourcelist "sources.list";
                       main "apt.conf";
                       preferences "preferences";
                   };
};

Debug::pkgProblemResolver="1";

RPM
{
    PM "external";
    Options { "--define";"_rpmlock_path %{instroot}/%{cmsplatf}/var/lib/rpm/lock";"--dbpath";"%{instroot}/var/lib/rpm";"--nodeps";};
    Install-Options { "--define";"_rpmlock_path %{instroot}/%{cmsplatf}/var/lib/rpm/lock";"--nodeps";"--force";"--dbpath";"%{instroot}/%{cmsplatf}/var/lib/rpm";"--prefix";"%{instroot}";};
    RootDir "%{instroot}";
    Architecture "%{cmsplatf}";
};
EOF_APT_CONF

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
                                        " > %{instroot}/bootstrap-%{cmsplatf}.sh

%post
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/apt/lists/partial
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/rpm 
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/cache/%{cmsplatf}/partial
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/apt
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/rpm
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/lib/apt/methods
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/dpkg/status
mkdir -p $RPM_INSTALL_PREFIX/bin
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/cache/%{cmsplatf}

cat << \EOF_BIN_APT_CACHE_WRAPPER > $RPM_INSTALL_PREFIX/bin/apt-cache-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-cache $@  
EOF_BIN_APT_CACHE_WRAPPER
chmod +x $RPM_INSTALL_PREFIX/bin/apt-cache-wrapper

cat << \EOF_BIN_APT_GET_WRAPPER > $RPM_INSTALL_PREFIX/bin/apt-get-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-get $@  
EOF_BIN_APT_GET_WRAPPER
chmod +x $RPM_INSTALL_PREFIX/bin/apt-get-wrapper

mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/apt
cat << \EOF_RPMPRIORITIES > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/apt/rpmpriorities
Essantial:

EOF_RPMPRIORITIES

cat << \EOF_SOURCES_LIST > $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/apt/sources.list
rpm http://cmsrep.cern.ch cms/cpt/Software/download/cms.eulisse/apt/%{cmsplatf} cms lcg external  
rpm-src http://cmsrep.cern.ch cms/cpt/Software/download/cms.eulisse/apt/%{cmsplatf} cms lcg external
# This are defined to support experimental repositories. The bootstrap file rewrites and uncomments
# them when passed the appropriate commandline option. 
## rpm @SERVER@ @SERVER_PATH@/@REPOSITORY@/apt/%{cmsplatf} @GROUPS@  
## rpm-src @SERVER@ @SERVER_PATH@/@REPOSITORY@/apt/%{cmsplatf} @GROUPS@
EOF_SOURCES_LIST

mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/var/lib/rpm

# FIXME: this is the ugliest trick ever found in a shell script.
# This is my understanding of the situation.
# apt runs internally as if --root != / while uses rpm with 
# --root $rootdir but --dbpath is always passed as $rootdir/$rpmdb.
# This way the rpm db is sometimes in $rootdir/$rpmdb, sometimes in
# $rootdir/$rootdir/$rpmdb and files are scattered around, causing
# big confusion. The solution is.... to create a link so that $rootdir/$rootdir
# is actually $rootdir. Clear, isn't it? If not, I don't blame you, but 
# this is the only way I could make it working. I need to look at the apt code to
# (and probably fix it) to understand it better. For the time being....
# TODO: check if this still applies with this version of apt-get
# TODO: check if we can fix the problem by patching apt sources.

firstdir=$(echo $RPM_INSTALL_PREFIX | cut -d/ -f1,2)
if [ -f $RPM_INSTALL_PREFIX$firstdir ] 
then
    echo "Hack to enable apt working as user"
    ln -sf $firstdir $RPM_INSTALL_PREFIX$firstdir
fi

%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|" $RPM_INSTALL_PREFIX/bin/apt-cache-wrapper $RPM_INSTALL_PREFIX/bin/apt-get-wrapper 
%files
%{i}
%{instroot}/bootstrap-%{cmsplatf}.sh
%{instroot}/%{cmsplatf}/var/lib/rpm


