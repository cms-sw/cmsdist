### RPM external apt 0.5.15lorg3.2
## INITENV SET APT_CONFIG %{i}/etc/apt/apt.conf

Source:  http://apt-rpm.org/releases/%n-%v.tar.bz2
Patch0: apt-rpm449
Requires: libxml2 beecrypt rpm zlib bz2lib
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

%post
mkdir -p %{cmsplatf}/var/lib/apt/lists/partial
mkdir -p %{cmsplatf}/var/lib/rpm 
mkdir -p %{cmsplatf}/var/lib/cache/%{cmsplatf}/partial
mkdir -p %{cmsplatf}/etc/apt
mkdir -p %{cmsplatf}/etc/rpm
mkdir -p %{cmsplatf}/lib/apt/methods
mkdir -p %{cmsplatf}/var/lib/dpkg/status
mkdir -p bin
mkdir -p %{cmsplatf}/var/lib/cache/%{cmsplatf}

cat << \EOF_BIN_APT_CACHE_WRAPPER > bin/apt-cache-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-cache $@  
EOF_BIN_APT_CACHE_WRAPPER
chmod +x bin/apt-cache-wrapper

cat << \EOF_BIN_APT_GET_WRAPPER > bin/apt-get-wrapper
#!/bin/sh
touch %{instroot}/log.txt
echo $@ >> %{instroot}/log.txt
apt-get $@  
EOF_BIN_APT_GET_WRAPPER
chmod +x bin/apt-get-wrapper

mkdir -p %{cmsplatf}/etc/apt
cat << \EOF_RPMPRIORITIES > %{cmsplatf}/etc/apt/rpmpriorities
Essantial:

EOF_RPMPRIORITIES

mkdir -p %{cmsplatf}/var/lib/rpm

%{relocateConfig}etc/profile.d/dependencies-setup.sh
%{relocateConfig}etc/profile.d/dependencies-setup.csh
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|" bin/apt-cache-wrapper bin/apt-get-wrapper 
