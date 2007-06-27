### RPM external glimpse 4.18.5-CMS3
Source: http://webglimpse.net/trial/glimpse-%{realversion}.tar.gz

%prep
%setup -n glimpse-%realversion
%build
./configure --prefix=%{i} 
# Turn off this part, it causes problems for 32-bit-on-64-bit and is only
# needed for webglimpse
perl -p -i -e "s|dynfilters||g" Makefile
make 

%install
make install
cat <<\EOF_CMS_GLIMPSE >%{i}/bin/cmsglimpse
#!/bin/bash
CURRENT_SCRAM_PROJECT=$(echo $SCRAMRT_SET | cut -d: -f2)
args=
action=

while [ $# -gt 0 ]
do
  case $1 in
    --full ) 
	action=full; shift;;
    --help )
	echo "cmsglimpse [-H <CMSSW_TAG>] [--full] [--help] [glimpse-options] <search term>" 
        echo ""
        echo "  -H <CMSSW_TAG> - specify the CMSSW tag for the release you    "
        echo "                   would like to search (e.g. 'CMSSW_1_0_0').   "
        echo "                   If you do not specify the -H option it will  "
        echo "                   default to the release corresponding to      "
        echo "                   your current scram runtime environment.      "
        echo ""
        echo "  --full         - Print the full path to the source files. The "
        echo "                   default is to print the relative path        "
        echo "                   beginning with the CMSSW subsystem.          " 
        echo ""
        echo "  --help         - This help information                        "
        echo ""
        echo "  [glimpse-options] - any of the glimpse options can also be    "
        echo "                      specified, except for -H and --help, which"
        echo "                      are used as described above.              "
        echo "                      See 'glimpse --help' for the full list.   "
	exit
	;;
    -H )[ $# -gt 1 ] || { echo "Option \`$1' requires an argument" 1>&2; exit 1;  }
	CURRENT_SCRAM_PROJECT=$2; shift; shift ;;
    * ) args="$args $1"; shift;;	
  esac
done

if [ "$CURRENT_SCRAM_PROJECT" == "" ]
then
	echo "No project specified. "
	echo "Please eval some scram runtime or use -H option."
	exit 1
fi

case $action in
	full )
		if [ ! -e @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src/.glimpse_full/.glimpse_index ]
		then 
			echo "Glimpse index not found. Expected it in directory:"
			echo "  @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src/.glimpse_full/"
			exit 1
                fi
		glimpse -H @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src/.glimpse_full/ $args
		;;
	* )
		if [ ! -e @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src/.glimpse_index ]
		then 
			echo "Glimpse index not found. Expected it in directory:"
			echo "  @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src/"
			exit 1
                fi
		glimpse -H @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT/src $args
		;;
esac
EOF_CMS_GLIMPSE
perl -p -i -e "s|\@CMSPLATF\@|%cmsplatf|g" %{i}/bin/cmsglimpse
chmod +x %{i}/bin/cmsglimpse
%post
perl -p -i -e "s|\@INSTROOT\@|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/%{pkgrel}/bin/cmsglimpse 
