### RPM configuration gsl-toolfile 1.5
## IMPORT scramtoolbox-common

Source: none
Requires: gsl

%build
%install
%define toolfilePath %toolBoxDir/General
mkdir -p %toolConfDir %toolfilePath

cat << \EOF_gsl_TOOLCONF_FRAGMENT > %toolConfDir/gsl.conf
TOOL:gsl
   +GSL_BASE:${GSL_ROOT}
   +PATH:${GSL_ROOT}/bin
   +LIBDIR:${GSL_ROOT}/lib
   +INCLUDE:${GSL_ROOT}/include
EOF_gsl_TOOLCONF_FRAGMENT

cat << \EOF_gsl_TOOLFILE > %toolfilePath/gsl
<doc type=BuildSystem::ToolDoc version=1.0>
<tool name=%toolname version=%v>
<info url="http://www.gnu.org/software/gsl/gsl.html"></info>
<lib name=gsl>
<lib name=gslcblas>
<client>
<environment name=GSL_BASE>
The top of the GNU Scientific Library distribution.
</environment>
<environment name=LIBDIR default="$GSL_BASE/lib" type=lib></environment>
<environment name=INCLUDE default="$GSL_BASE/include"></environment>
</client>
<environment name=LD_LIBRARY_PATH value="$LIBDIR" type=Runtime_path></environment>
<architecture name=win>
<environment name=PATH value="$LIBDIR" type=Runtime_path></environment>
</architecture>
</tool>

EOF_gsl_TOOLFILE
%files
%toolfilePath/gsl
%toolConfDir/gsl.conf
