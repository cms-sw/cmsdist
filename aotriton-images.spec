## INCLUDE aotriton/version
### RPM external aotriton-images %{aotriton_tag}
## NOCOMPILER
AutoReqProv: no

Source0: https://github.com/ROCm/aotriton/releases/download/0.13b/aotriton-%{realversion}-images-amd-gfx942.tar.gz
Source1: https://github.com/ROCm/aotriton/releases/download/0.13b/aotriton-%{realversion}-images-amd-gfx90a.tar.gz
Source2: https://github.com/ROCm/aotriton/releases/download/0.13b/aotriton-%{realversion}-images-amd-gfx110x.tar.gz

%prep
for amd_gpu in $(echo "%{rocm_archs}" | tr ' ' '\n' | sed 's|:.*||') ; do
  case $amd_gpu in
    gfx1100|gfx1102) amd_gpu=gfx110x ;;
    * ) ;;
  esac
  tar -xzvf %{_sourcedir}/aotriton-%{realversion}-images-amd-${amd_gpu}.tar.gz
done

%build

%install
mv aotriton/lib/aotriton.images %{i}/aotriton.images
