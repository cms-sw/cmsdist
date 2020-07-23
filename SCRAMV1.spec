### RPM lcg SCRAMV1 V2_2_9_pre07
## NOCOMPILER

BuildRequires: gmake

Provides: perl(BuildSystem::Template::Plugins::PluginCore)
Provides: perl(BuildSystem::TemplateStash)
Provides: perl(Cache::CacheUtilities)
Provides: perl(BuildSystem::ToolManager)

%define tag %{realversion}
%define branch master
%define github_user cms-sw
Source: git+https://github.com/%{github_user}/SCRAM.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}-%{tag}.tgz

%define OldDB /%{cmsplatf}/lcg/SCRAMV1/scramdb/project.lookup
%define SCRAM_ALL_VERSIONS   V[0-9][0-9]*_[0-9][0-9]*_[0-9][0-9]*
%define SCRAM_REL_MINOR      %(echo %realversion | grep '%{SCRAM_ALL_VERSIONS}' | sed 's|^\\(V[0-9][0-9]*_[0-9][0-9]*\\)_.*|\\1|')
%define SCRAM_REL_MAJOR      %(echo %realversion | sed 's|^\\(V[0-9][0-9]*\\)_.*|\\1|')
%define SetLatestVersion \
  vers="" \
  for ver in `find %{pkgcategory}/%{pkgname} -maxdepth 2 -mindepth 2 -name "bin" -type d | sed 's|/bin$||' | xargs -I '{}' basename '{}' | grep "$VERSION_REGEXP" `; do \
    ver_str=`echo $ver | sed 's|-.\\+$||' | tr '_' '\\n' | sed 's|V\\([0-9]\\)$|V0\\1|;s|^\\([0-9]\\)$|0\\1|' | tr '\\n' '_'` \
    vers="${ver_str}zzz:${ver} ${vers}" \
  done \
  echo $vers | tr ' ' '\\n' | grep -v '^$' | sort  | tail -1 | sed 's|.*:||' > etc/$VERSION_FILE \
  [ -s etc/$VERSION_FILE ] || rm -f etc/$VERSION_FILE

%define BackwardCompatibilityVersionPolicy \
  touch etc/default-scram/%{SCRAM_REL_MINOR} \
  for ver in `find etc/default-scram -maxdepth 1 -mindepth 1 -name "%{SCRAM_REL_MAJOR}_[0-9]*" -type f |  xargs -I '{}' basename '{}' | grep 'V[0-9][0-9]*_[0-9][0-9]*$' `; do \
    case $ver in \
      V2_[01] ) ;;\
      * ) \
        if [ -f etc/default-scram/%{SCRAM_REL_MAJOR} ] ; then \
          cp etc/default-scram/%{SCRAM_REL_MAJOR} etc/default-scram/$ver \
        else\
          rm -f etc/default-scram/$ver \
        fi;;\
      esac \
  done

%prep
#SCRAM version policy check
if [ "X%{SCRAM_REL_MINOR}" == "X" ] ; then 
  echo "You are trying to build SCRAM version %v which does not follow the SCRAM version policy. Valid SCRAM versions should be of the form V[0-9]+_[0-9]+_[0-9].*"
  exit 1
fi

%setup -n %{n}-%{realversion}
%build
gmake %{makeprocesses} all INSTALL_BASE=%{instroot} VERSION=%{realversion} PREFIX=%{i}

%install
gmake %{makeprocesses} install INSTALL_BASE=%{instroot} VERSION=%{realversion} PREFIX=%{i}

%post
%{relocateRpmPkg}bin/scram
sed -i -e "s|dbPath = '$RPM_INSTALL_PREFIX';|dbPath = '$CMS_INSTALL_PREFIX';|" $RPM_INSTALL_PREFIX/%{pkgrel}/bin/scram
echo "SCRAMV1_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "SCRAMV1_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.sh
echo "set SCRAMV1_ROOT='$CMS_INSTALL_PREFIX/%{pkgrel}'" > $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh
echo "set SCRAMV1_VERSION='%v'" >> $RPM_INSTALL_PREFIX/%{pkgrel}/etc/profile.d/init.csh

if [ ! -d $RPM_INSTALL_PREFIX/etc/scramrc ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/etc/scramrc
  touch $RPM_INSTALL_PREFIX/etc/scramrc/links.db
  echo 'CMSSW=$SCRAM_ARCH/cms/cmssw/CMSSW_*'       > $RPM_INSTALL_PREFIX/etc/scramrc/cmssw.map
  echo 'CMSSW=$SCRAM_ARCH/cms/cmssw-patch/CMSSW_*' > $RPM_INSTALL_PREFIX/etc/scramrc/cmssw-patch.map
  echo 'CORAL=$SCRAM_ARCH/cms/coral/CORAL_*'       > $RPM_INSTALL_PREFIX/etc/scramrc/coral.map
  [ ! -f $RPM_INSTALL_PREFIX/%{OldDB} ] || grep '%{OldDB} *$' $RPM_INSTALL_PREFIX/%{OldDB} | awk '{print $2}' | sed 's|%{OldDB}.*||' > $RPM_INSTALL_PREFIX/etc/scramrc/links.db
fi

touch $RPM_INSTALL_PREFIX/etc/scramrc/site.cfg
mkdir -p $RPM_INSTALL_PREFIX/%{cmsplatf}/etc/default-scram $RPM_INSTALL_PREFIX/share/etc/default-scram
cd $RPM_INSTALL_PREFIX/%{cmsplatf}
VERSION_REGEXP="%{SCRAM_ALL_VERSIONS}" ; VERSION_FILE=default-scramv1-version         ; %{SetLatestVersion}
VERSION_REGEXP="%{SCRAM_REL_MAJOR}_"   ; VERSION_FILE=default-scram/%{SCRAM_REL_MAJOR}; %{SetLatestVersion}
%{BackwardCompatibilityVersionPolicy}

#Create a shared copy of this version
if [ ! -d $RPM_INSTALL_PREFIX/share/%{pkgdir} ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/share/%{pkgdir}
  rsync --links --ignore-existing --recursive --exclude='etc/'  $RPM_INSTALL_PREFIX/%{pkgrel}/ $RPM_INSTALL_PREFIX/share/%{pkgdir}
  for f in `rsync --links --ignore-existing --recursive --itemize-changes $RPM_INSTALL_PREFIX/%{pkgrel}/etc $RPM_INSTALL_PREFIX/share/%{pkgdir} | grep '^>f' | sed -e 's|.* ||'` ; do
    sed -i -e 's|/%{pkgrel}|/share/%{pkgdir}|g' $RPM_INSTALL_PREFIX/share/%{pkgdir}/$f
  done
fi

cd $RPM_INSTALL_PREFIX/share
VERSION_REGEXP="%{SCRAM_ALL_VERSIONS}" ; VERSION_FILE=default-scramv1-version         ; %{SetLatestVersion}
VERSION_REGEXP="%{SCRAM_REL_MAJOR}_"   ; VERSION_FILE=default-scram/%{SCRAM_REL_MAJOR}; %{SetLatestVersion}

if [ `cat $RPM_INSTALL_PREFIX/share/etc/default-scramv1-version` == '%v' ] ; then
  mkdir -p $RPM_INSTALL_PREFIX/share/man/man1
  cp -f $RPM_INSTALL_PREFIX/share/%{pkgdir}/docs/man/man1/scram.1 ${RPM_INSTALL_PREFIX}/share/man/man1/scram.1
fi

#FIMEME: Remove it when cmsBuild has a fix
#For some strange reason we need something after the last statement
#otherwise RPM does not run it. rpm -q --scripts also confirm that above
#command is missing if there is nothing after the last multi-line macro

%postun
rm -rf $RPM_INSTALL_PREFIX/%{pkgrel} || true
cd $RPM_INSTALL_PREFIX/%{cmsplatf}
VERSION_REGEXP="%{SCRAM_ALL_VERSIONS}"; VERSION_FILE=default-scramv1-version         ; %{SetLatestVersion}
VERSION_REGEXP="%{SCRAM_REL_MAJOR}_"  ; VERSION_FILE=default-scram/%{SCRAM_REL_MAJOR}; %{SetLatestVersion}
%{BackwardCompatibilityVersionPolicy}
