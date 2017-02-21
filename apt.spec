### RPM external apt 0.5.19
## INITENV SET APT_CONFIG %{i}/etc/apt.conf
## INITENV CMD_SH  if [ -f %{instroot}/common/apt-site-env.sh  ]; then . %{instroot}/common/apt-site-env.sh;  fi
## INITENV CMD_CSH if ( -f %{instroot}/common/apt-site-env.csh )  source %{instroot}/common/apt-site-env.csh; endif
## NOCOMPILER

Source0: git://github.com/cms-sw/apt-rpm.git?obj=master/%{realversion}&export=apt-rpm-%{realversion}&output=/apt-rpm-%{realversion}.tgz
# svn://svn.github.com/ktf/apt-rpm.git?scheme=http&revision=%{realversion}&module=apt-rpm&output=/apt-rpm.tar.gz
Source1: bootstrap
Source2: http://search.cpan.org/CPAN/authors/id/T/TL/TLBDK/RPM-Header-PurePerl-1.0.2.tar.gz

Requires: rpm
BuildRequires: gcc

%prep
%setup -T -b 2 -n RPM-Header-PurePerl-1.0.2
cd ..
%setup -n apt-rpm-%{realversion}

%build
case %cmsplatf in
  slc*_amd64_*)
    export USER_CFLAGS="-pthread"
    export USER_CXXFLAGS="-pthread"
    export USER_LDFLAGS="-pthread"
    export USER_LIBS="-pthread"
    export USER_RPM_LIBS="-ldl"
    ;;
  slc*_aarch64_*|fc*)
    export USER_RPM_LIBS="-ldl -lrt -pthread"
    ;;
  *) ;;
esac

chmod +x buildlib/install-sh
# Avoid picking up sqlite3 from the system.
perl -p -i -e 's|sqlite3|sqlite3disabled|' configure
./configure --prefix=%{i} --exec-prefix=%{i} \
                          --build="%{_build}" \
                          --host="%{_host}" \
                          --disable-static \
                          --disable-nls \
                          --disable-dependency-tracking \
                          --without-libintl-prefix \
                          --disable-docs \
                          --disable-selinux \
                          --disable-rpath \
                          CXXFLAGS="-fPIC $USER_CXXFLAGS" \
                          CFLAGS="-fPIC $USER_CFLAGS" \
                          CPPFLAGS="-DAPT_DISABLE_MULTIARCH -D_RPM_4_4_COMPAT -I$BOOTSTRAP_BUNDLE_ROOT/include -I$RPM_ROOT/include -I$RPM_ROOT/include/rpm $USER_CPPFLAGS" \
                          LDFLAGS="-L$BOOTSTRAP_BUNDLE_ROOT/lib -L$RPM_ROOT/lib $USER_LDFLAGS" \
                          libs="-llua $USER_LIBS" \
                          LIBXML2_CFLAGS="-I$BOOTSTRAP_BUNDLE_ROOT/include/libxml2 -I$BOOTSTRAP_BUNDLE_ROOT/include -I$RPM_ROOT/include" \
                          LIBXML2_LIBS="-lxml2 -L$BOOTSTRAP_BUNDLE_ROOT/lib -L$RPM_ROOT/lib" \
                          RPM_LIBS="-L$RPM_ROOT/lib -lrpm -lrpmio -lrpmbuild $USER_RPM_LIBS"

chmod +x buildlib/install-sh
make %{makeprocesses}


%install
make install
case %cmsos in
  osx*) SONAME=dylib ;;
  *) SONAME=so ;;
esac
# Drop documentation and developer files, since we do not need it.
%define drop_files %i/{share,include}
# Strip executables and libraries.
%define strip_files %i/lib %i/bin/{apt-config,genpkglist,apt-get,countpkglist,gensrclist,apt-cache,apt-shell} %i/lib/apt/methods/*
# Remove pkg-config to avoid rpm-generated dependency on /usr/bin/pkg-config
# which we neither need nor use at this time.
rm -rf %i/lib/pkgconfig

mkdir -p %{i}/etc/profile.d

(echo "#!/bin/sh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.sh"  ) > %{i}/etc/profile.d/dependencies-setup.sh
(echo "#!/bin/tcsh"; \
 echo "source $RPM_ROOT/etc/profile.d/init.csh" ) > %{i}/etc/profile.d/dependencies-setup.csh

cp %_sourcedir/bootstrap %{i}/bin/bootstrap.sh
perl -p -i -e 'my $s = `cat ../RPM-Header-PurePerl-1.0.2/lib/RPM/Header/PurePerl.pm`;\
               s|\@RPM_HEADER_PUREPERL_PM\@|$s|' %{i}/bin/bootstrap.sh
perl -p -i -e 'my $s = `cat ../RPM-Header-PurePerl-1.0.2/lib/RPM/Header/PurePerl/Tagtable.pm`;\
               s|\@RPM_HEADER_PUREPERL_TAGSTABLE_PM\@|$s|' %{i}/bin/bootstrap.sh

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

APT::Cache-Limit 33554432;
APT::http::Max-Age 0;

Acquire::Retries 5;
EOF_APT_CONF


cat << \EOF_SOURCES_LIST > %{i}/etc/sources.list
rpm http://cmsrep.cern.ch cms/cpt/Software/download/cms/apt/%{cmsplatf} cms lcg external
# rpm-src http://cmsrep.cern.ch cms/cpt/Software/download/cms/apt/%{cmsplatf} cms lcg external
# This are defined to support experimental repositories. The bootstrap file rewrites and uncomments
# them when passed the appropriate commandline option. 
#;rpm http://@SERVER@ @SERVER_PATH@@REPOSITORY@/apt/%{cmsplatf} @GROUPS@  
# rpm-src http://@SERVER@ @SERVER_PATH@@REPOSITORY@/apt/%{cmsplatf} @GROUPS@
EOF_SOURCES_LIST

cat << \EOF_RPMPRIORITIES > %{i}/etc/rpmpriorities
Essantial:

EOF_RPMPRIORITIES

cat << \EOF_BIN_APT_CACHE_WRAPPER > %{i}/bin/apt-cache-wrapper
#!/bin/sh
mkdir -p %{instroot}/var/log/rpm
touch %{instroot}/var/log/rpm/log.txt
echo $@ >> %{instroot}/var/log/rpm/log.txt
apt-cache $@
EOF_BIN_APT_CACHE_WRAPPER
chmod +x %{i}/bin/apt-cache-wrapper

cat << \EOF_BIN_APT_GET_WRAPPER > %{i}/bin/apt-get-wrapper
#!/bin/sh
mkdir -p %{instroot}/var/log/rpm
touch %{instroot}/var/log/rpm/log.txt
echo $@ >> %{instroot}/var/log/rpm/log.txt
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
mkdir -p %{instroot}/var/log/rpm
touch %{instroot}/var/log/rpm/log.txt
echo rpm ${1+"$@"} >> %{instroot}/var/log/rpm/log.txt
exec rpm ${1+"$@"}
EOF_BIN_RPM
chmod +x %{i}/bin/rpm-wrapper
mkdir -p %{instroot}/%{cmsplatf}/var/lib/apt/lists/partial
mkdir -p %{instroot}/%{cmsplatf}/var/lib/rpm 
mkdir -p %{instroot}/%{cmsplatf}/var/lib/cache/%{cmsplatf}/partial
mkdir -p %{instroot}/%{cmsplatf}/var/lib/dpkg/status
mkdir -p %{instroot}/%{cmsplatf}/etc/rpm
mkdir -p %{instroot}/%{cmsplatf}/lib/apt/methods

%post
%{relocateRpmPkg}etc/profile.d/dependencies-setup.*
%{relocateRpmPkg}bin/apt-cache-wrapper
%{relocateRpmPkg}bin/apt-get-wrapper
%{relocateRpmPkg}bin/rpm-wrapper
%{relocateRpmPkg}etc/apt.conf
