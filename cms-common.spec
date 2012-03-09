### RPM cms cms-common 1.0
## REVISION 1058
## NOCOMPILER
%define online %(case %cmsplatf in (*onl_*_*) echo true;; (*) echo false;; esac)
Source: cmsos
%prep
%build
echo $SCRAM_ROOT
%install

mkdir -p %instroot/common %instroot/bin %instroot/%{cmsplatf}/etc/profile.d

# Do not create these common files if already exist 
# This is to avoid different arch creating these files
if [ ! -f %instroot/common/.cms-common ]; then
install -m 755 %_sourcedir/cmsos %instroot/common/cmsos
### Detects the SCRAM_ARCH to be used.
%if "%online" != "true"
cat << \EOF_CMSARCH_SH >%instroot/common/cmsarch
#!/bin/sh
osarch=`%instroot/common/cmsos`
compilerv=gcc434
# We need to assume 1 compiler per platform. 
# There is no other way around this.
if [ ! "$SCRAM_ARCH" ]
then
    case $osarch in
        osx104_ia32) compilerv=gcc401;;
        osx104_ppc32) compilerv=gcc400;;
        osx105_*) compilerv=gcc401;;
        osx106_*) compilerv=gcc421;;
        slc6_*) compilerv=gcc461; osarch=slc6_amd64;;
        slc5_*) compilerv=gcc434; osarch=slc5_amd64;;
        slc4_*) compilerv=gcc345; osarch=slc4_ia32;;
        *) compilerv=gcc434; osarch=slc5_ia32;;
    esac
    echo ${osarch}_${compilerv}
else
    echo $SCRAM_ARCH
fi

EOF_CMSARCH_SH
%else
cat << \EOF_CMSARCH_SH >%instroot/common/cmsarch
#!/bin/sh
if [ ! "$SCRAM_ARCH" ] ; then
    echo %cmsplatf
else
    echo $SCRAM_ARCH
fi

EOF_CMSARCH_SH
%endif
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
alias cmsenv='eval `scramv1 runtime -sh`'
alias cmsrel='scramv1 project CMSSW'

if [ -f $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.sh ]; then
        . $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.sh
fi

if [ ! $CVSROOT ]
then
    CVSROOT=:gserver:cmssw.cvs.cern.ch:/cvs/CMSSW
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
alias cmsenv 'eval `scramv1 runtime -csh`'
alias cmsrel 'scramv1 project CMSSW'

if( -e $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.csh ) then 
        source $CMS_PATH/SITECONF/local/JobConfig/cmsset_local.csh
endif

if ( ! ${?CVSROOT}) then
  setenv CVSROOT :gserver:cmssw.cvs.cern.ch:/cvs/CMSSW
endif

unset here
EOF_CMSSET_DEFAULT_CSH

cat << \EOF_COMMON_SCRAM > %instroot/common/scram
#!/bin/sh
CMSARCH=`cmsarch`
srbase=%{instroot}/$CMSARCH
sver=$SCRAM_VERSION
dir=`/bin/pwd`
while [ ! -d ${dir}/.SCRAM ] && [ "$dir" != "/" ] ; do
  dir=`dirname $dir`
done
if [ -f ${dir}/config/scram_version ] ; then
  sver=`cat ${dir}/config/scram_version`
elif [ "X$sver" = "X" ] ; then
  sver=`cat  ${srbase}/etc/default-scramv1-version`
fi
if [ "X$sver" = "XV1_0_3-p1" ] && [ "X$CMSARCH" = "Xslc4_ia32_gcc345" ] ; then
  sver=V1_0_3-p2
fi
scram_rel_series=`echo $sver | grep '^V[0-9]\+_[0-9]\+_[0-9]\+' | sed 's|^\(V[0-9]\+_[0-9]\+\)_.*|\1|'`
if [ "X${scram_rel_series}" != "X" ] && [ -f ${srbase}/etc/default-scram/${scram_rel_series} ] ; then
  sver=`cat ${srbase}/etc/default-scram/${scram_rel_series}`
fi
scmd=scram
srbase=%{instroot}/$CMSARCH/lcg/SCRAMV1
case $sver in
  V0_*  ) srbase=%{instroot}/$CMSARCH/lcg/SCRAM; scmd=scramv0;;
  V1_0* ) scmd=scramv1;;
  *     ) ;;
esac
if [ ! -f ${srbase}/${sver}/etc/profile.d/init.sh ] ; then
  echo "Unable to find SCRAM version $sver for $CMSARCH architecture."
  exit 1
fi
. ${srbase}/${sver}/etc/profile.d/init.sh
# In the case we are on linux ia32 we prepend the linux32 command to the 
# actual scram command so that, no matter where the ia32 architecture is 
# running (i686 or x84_64) scram detects it as ia32.
CMSPLAT=`echo $CMSARCH | cut -d_ -f 2`
USE_LINUX32=
if [ `uname` = "Linux" ] && [ "$CMSPLAT" = "ia32" ] ; then
  USE_LINUX32=linux32
fi
$USE_LINUX32 ${srbase}/${sver}/bin/${scmd} $@
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
echo $CMS_INSTALL_PREFIX
%{relocateCmsFiles} $RPM_INSTALL_PREFIX/cmsset_default.sh
%{relocateCmsFiles} $RPM_INSTALL_PREFIX/cmsset_default.csh
%{relocateCmsFiles} $RPM_INSTALL_PREFIX/common/cmsos
%{relocateCmsFiles} $RPM_INSTALL_PREFIX/common/cmsarch
%{relocateCmsFiles} $RPM_INSTALL_PREFIX/common/scram

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
