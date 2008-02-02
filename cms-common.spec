### RPM cms cms-common 1.0 
Source: cmsos
%prep
%build
echo $SCRAM_ROOT
%install

mkdir -p %instroot/common %instroot/bin %{instroot}/%{cmsplatf}/etc/profile.d

# Do not create these common files if already exist
# This is to avoid different arch creating these files
if [ ! -f %instroot/common/.cms-common ]; then
install -m 755 %_sourcedir/cmsos %instroot/common/cmsos
### Detects the SCRAM_ARCH to be used.
cat << \EOF_CMSARCH_SH >%instroot/common/cmsarch
#!/bin/sh
osarch=`%instroot/common/cmsos`
compilerv=gcc323
# We need to assume 1 compiler per platform. 
# There is no other way around this.
if [ ! "$SCRAM_ARCH" ]
then
    case $osarch in
        slc3_ia32) compilerv=gcc323;;
        slc3_amd64) compilerv=gcc344;;
        slc4_ia32) compilerv=gcc345;;
        slc4_amd64) compilerv=gcc345; osarch=slc4_ia32;;
        osx104_ia32) compilerv=gcc401;;
        osx104_ppc32) compilerv=gcc400;;
    esac
    echo ${osarch}_${compilerv}
else
    echo $SCRAM_ARCH
fi

EOF_CMSARCH_SH
chmod 755 %instroot/common/cmsarch

### BASH code

cat << \EOF_CMSSET_DEFAULT_SH > %instroot/cmsset_default.sh
export PATH=%instroot/common:%instroot/bin:$PATH

if [ ! $SCRAM_ARCH ]
then
    SCRAM_ARCH=`%instroot/common/cmsarch`
    export SCRAM_ARCH
fi

here=%{instroot}

if [ "$VO_CMS_SW_DIR" != ""  ] 
then
    here=$VO_CMS_SW_DIR
else
    if [ "$OSG_APP" != "" ]
    then
        here=$OSG_APP/cmssoft/cms
    fi
fi

if [ ! -d $here/${SCRAM_ARCH}/etc/profile.d ] 
then
    echo "Your shell is not able to find where cmsset_default.sh is located." 
    echo "Either you have not set VO_CMS_SW_DIR or OSG_APP correctly"
    echo "or SCRAM_ARCH is not set to a valid architecture."
fi

for pkg in `/bin/ls $here/${SCRAM_ARCH}/etc/profile.d/ | grep 'S.*[.]sh'`
do
	source $here/${SCRAM_ARCH}/etc/profile.d/$pkg
done

if [ ! $CMS_PATH ]
then
    export CMS_PATH=$here
fi

# aliases
alias cmsenv='eval `scram runtime -sh`'
alias cmsrel='scram project CMSSW'

if [ -f $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.sh ]; then
        . $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.sh
fi

if [ ! $CVSROOT ]
then
    CVSROOT=:kserver:cmscvs.cern.ch:/cvs_server/repositories/CMSSW
    export CVSROOT
fi

EOF_CMSSET_DEFAULT_SH


### CSH code

cat << \EOF_CMSSET_DEFAULT_CSH > %instroot/cmsset_default.csh

if (${?PATH}) then
    setenv PATH %instroot/common:%instroot/bin:$PATH
else
    setenv PATH %instroot/common:%instroot/bin
endif

if ( ! ${?SCRAM_ARCH}) then
    setenv SCRAM_ARCH `sh -c %instroot/common/cmsarch` 
endif

set here=%instroot 

if ( ${?VO_CMS_SW_DIR} ) then
    set here=$VO_CMS_SW_DIR
else
    # OSG
    if ( ${?OSG_APP} ) then
        set here=$OSG_APP/cmssoft/cms
    endif
    # OSG                       
endif

if ( ! -e $here/cmsset_default.csh ) then
    echo "Please cd into the directory where cmsset_default.csh is."
endif

foreach pkg ( `/bin/ls ${here}/${SCRAM_ARCH}/etc/profile.d/ | grep 'S.*[.]csh'` )
	source ${here}/${SCRAM_ARCH}/etc/profile.d/$pkg
end
if ( ! ${?CMS_PATH} ) then
    setenv CMS_PATH $here
endif

# aliases
alias cmsenv 'eval `scram runtime -csh`'
alias cmsrel 'scram project CMSSW'

if( -e $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.csh ) then 
        source $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.csh
endif

if ( ! ${?CVSROOT}) then
  setenv CVSROOT :kserver:cmscvs.cern.ch:/cvs_server/repositories/CMSSW
endif

unset here
EOF_CMSSET_DEFAULT_CSH

cat << \EOF_COMMON_SCRAM > %instroot/common/scram
#!/bin/sh
CMSARCH=`cmsarch`
srbase=
if [ "X$SCRAM_VERSION" = "X" ] ; then
  sver=`cat  %{instroot}/$CMSARCH/etc/default-scramv1-version`
  dir=`/bin/pwd`
  while [ ! -d ${dir}/.SCRAM -a "$dir" != "/" ] ; do
    dir=`dirname $dir`
  done
  if [ -f ${dir}/config/scram_version ] ; then
    ver=`cat ${dir}/config/scram_version`
    case $ver in
      V0_* ) srbase=lcg/SCRAM/${ver};;
      * ) srbase=lcg/SCRAMV1/${ver};;
    esac
    if [ -f %{instroot}/$CMSARCH/${srbase}/etc/profile.d/init.sh ] ; then
      sver=$ver
    fi
  fi
else
   sver=$SCRAM_VERSION
fi
scmd=scram
case $sver in
  V0_* ) srbase=lcg/SCRAM/${sver}; scmd=scramv0;;
  V1_0* ) srbase=lcg/SCRAMV1/${sver}; scmd=scramv1;;
  * ) srbase=lcg/SCRAMV1/${sver};;
esac
source %{instroot}/$CMSARCH/${srbase}/etc/profile.d/init.sh
# In the case we are on linux ia32 we prepend the linux32 command to the 
# actual scram command so that, no matter where the ia32 architecture is 
# running (i686 or x84_64) scram detects it as ia32.
CMSPLAT=`echo $CMSARCH | cut -d_ -f 2`
USE_LINUX32=
if [ `uname` == Linux ]; then
  if [ "$CMSPLAT" = "ia32" ]
  then
      USE_LINUX32=linux32
  fi
fi
$USE_LINUX32 %{instroot}/$CMSARCH/${srbase}/bin/${scmd} $@
EOF_COMMON_SCRAM

chmod +x %{instroot}/common/scram
ln -sf scram %{instroot}/common/scramv1
ln -sf scram %{instroot}/common/scramv0
ln -sf ../common/cmsarch %instroot/bin/cmsarch
ln -sf ../common/cmsarch %instroot/bin/cmsos
ln -sf ../common/scramv1 %instroot/bin/scramv1
touch %instroot/common/.cms-common
fi

touch %instroot/%cmsplatf/etc/profile.d/dummy

%post
echo $RPM_INSTALL_PREFIX
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/cmsset_default.sh
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/cmsset_default.csh
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/common/cmsos
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/common/cmsarch
perl -p -i -e "s|%{instroot}|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/common/scram

%files
%i
%instroot/cmsset_default.sh
%instroot/cmsset_default.csh
%instroot/common/cmsos
%instroot/common/cmsarch
%instroot/common/scram
%instroot/common/scramv1
%instroot/common/scramv0
%instroot/common/.cms-common
%instroot/bin/cmsos
%instroot/bin/cmsarch
%instroot/bin/scramv1
%instroot/%cmsplatf/etc/profile.d
%exclude %instroot/%cmsplatf/etc/profile.d/*
