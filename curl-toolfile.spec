### RPM external curl-toolfile 1.0
%define mic %(case %cmsplatf in (*_mic_*) echo true;; (*) echo false;; esac)
Requires: curl
%prep

%build

%install

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/curl.xml
<tool name="curl" version="@TOOL_VERSION@">
  <lib name="curl"/>
  <client>
    <environment name="CURL_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE"      default="$CURL_BASE/include"/>
    <environment name="LIBDIR"       default="$CURL_BASE/lib"/>
  </client>
%if "%mic" == "true"
  <runtime name="MIC_SRTOPT_PATH" value="$CURL_BASE/bin" type="path"/>
%else
  <runtime name="PATH" value="$CURL_BASE/bin" type="path"/>
%endif
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
