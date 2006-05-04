### RPM cms PHEDEX PHEDEX_2_3_0_pre1
Source: cvs://:pserver:anonymous@cmscvs.cern.ch:2401/cvs_server/repositories/CMSSW?passwd=AA_:yZZ3e&module=%n&export=%n&&tag=-r%{v}&output=/%n.tar.gz
Requires: oracle oracle-env p5-time-hires p5-text-glob p5-compress-zlib p5-dbi p5-dbd-oracle

%prep
%setup -n %n
%build
%install
(cd %_sourcedir/%n && tar -cf - * | (cd %i && tar -xf -)
