### RPM external glimpse 4.18.5
Source: http://webglimpse.net/trial/glimpse-%{v}.tar.gz

%prep
%setup -n glimpse-%v
%build
./configure --prefix=%{i} 
make 

%install
make install
cat <<\EOF_CMS_GLIMPSE >%{instroot}/bin/cmsglimpse
#!/bin/bash
CURRENT_SCRAM_PROJECT=$(echo $SCRAMRT_SET | cut -d: -f2)
args=
action=

while [ $# -gt 0 ]
do
  case $1 in
    -index ) [ $# -gt 1 ] || { echo "Option \`$1' requires an argument" 1>&2; exit 1;  } 
	action=index; shift;;

    -help )
	echo "cmsglimpse [-H <CMSSW_TAG>] <search term>"
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

GLIMPSE_DIR=@INSTROOT@/share/glimpse/$CURRENT_SCRAM_PROJECT

if [ -d $GLIMPSE_DIR ]
then
	echo "Glimpse index directory '$GLIMPSE_DIR' not found."
	echo "Try running cmsglimpse -index"
	exit 1
fi

case $action in
	index )
		(cd @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT; \
		 eval `scramv1 run -sh`;		 
		 glimpseindex $args -H $CURRENT_SCRAM_PROJECT @INSTROOT@/@CMSPLATF@/cms/cmssw/$CURRENT_SCRAM_PROJECT;)
		;;
	* )
		glimpse -H $CURRENT_SCRAM_PROJECT $args
		;;
esac
EOF_CMS_GLIMPSE
perl -p -i -e "s|\@CMSPLATF\@|%cmsplatf|g" %instroot/bin/cmsglimpse
chmod +x %{instroot}/bin/cmsglimpse
%post
perl -p -i -e "s|\@INSTROOT\@|$RPM_INSTALL_PREFIX|g" $RPM_INSTALL_PREFIX/bin/cmsglimpse 
