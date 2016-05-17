### RPM external jemalloc-toolfile 1.0
Requires: jemalloc 

%if %(case %{cmsplatf} in (*_aarch64_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define cmsplatf_aarch64 1
%endif

%if %(case %{cmsplatf} in (*_ppc64le_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define cmsplatf_ppc64le 1
%endif

%if %(case %{cmsplatf} in (*_ppc64_*) echo 1 ;; (*) echo 0 ;; esac) == 1
%define cmsplatf_ppc64 1
%endif

%prep

%build

%install

%if 0%{?cmsplatf_aarch64}%{?cmsplatf_ppc64le}%{?cmsplatf_ppc64}
# 64K page systems
%define jemalloc_config lg_chunk:23,lg_dirty_mult:8
%else
# 4K page systems
%define jemalloc_config lg_chunk:18,lg_dirty_mult:4
%endif

mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/jemalloc.xml
<tool name="jemalloc" version="@TOOL_VERSION@">
  <architecture name="slc.*|fc.*">
    <lib name="jemalloc"/>
  </architecture>
  <client>
    <environment name="JEMALLOC_BASE" default="@TOOL_ROOT@"/>
    <environment name="LIBDIR"        default="$JEMALLOC_BASE/lib"/>
    <environment name="INCLUDE"        default="$JEMALLOC_BASE/include"/>
  </client>
  <runtime name="MALLOC_CONF" value="%{jemalloc_config}"/>
  <runtime name="ROOT_INCLUDE_PATH" value="$INCLUDE" type="path"/>
  <use name="root_cxxdefaults"/>
</tool>
EOF_TOOLFILE

## IMPORT scram-tools-post
