### RPM cms cms_oracleocci_abi_hack-toolfile 1.1
Requires: cms_oracleocci_abi_hack

%define cms_oracleocci_libname cms_oracleocci_abi_hack
%define isdarwin %(case %{cmsos} in (osx*) echo 1 ;; (*) echo 0 ;; esac)
%define soext so
%if %isdarwin
%define soext dylib
%endif

%prep

%build

%install

mkdir -p %i/etc/scram.d
if [ -e ${CMS_ORACLEOCCI_ABI_HACK_ROOT}/lib/lib%{cms_oracleocci_libname}.%{soext} ] ; then
  export CMS_ORACLEOCCI_LIB='<lib name="%{cms_oracleocci_libname}"/>'
  export CMS_ORACLEOCCI_LIBDIR='<environment name="LIBDIR" value="$ORACLEOCCI_BASE/lib"/>'
  export CMS_ORACLEOCCI_LD_PRELOAD='<runtime name="CMS_ORACLEOCCI_LIB" value="$LIBDIR/lib%{cms_oracleocci_libname}.%{soext}"/>'
fi
cat << \EOF_TOOLFILE >%i/etc/scram.d/oracleocci.xml
<tool name="oracleocci" version="@TOOL_VERSION@">
  @CMS_ORACLEOCCI_LIB@
  <use name="oracleocci-official"/>
  <client>
    <environment name="ORACLEOCCI_BASE" default="@TOOL_ROOT@"/>
    <environment name="INCLUDE" value="$ORACLEOCCI_BASE/include"/>
    @CMS_ORACLEOCCI_LIBDIR@
  </client>
  @CMS_ORACLEOCCI_LD_PRELOAD@
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
# bla bla
