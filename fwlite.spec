### RPM cms fwlite CMSSW_7_6_1_FWLITE

Requires: fwlite-tool-conf python

%define saveDeps        yes
%define branch          CMSSW_7_0_X
%define gitcommit       %(echo %realversion | sed -e 's|_FWLITE||')

# Switch off building tests
%define patchsrc perl -p -i -e ' s|(<classpath.*test\\+test.*>)||;' config/BuildFile.xml*

# depends on MessageService, which pulls in service dependencies
%define patchsrc3 rm -f src/FWCore/MessageLogger/python/MessageLogger_cfi.py


# depends on CondFormats/EgammaObjects/interface/GBRForest.h which pulls in to many dependencies for fwlite
%define patchsrc4 rm -f src/CommonTools/Utils/src/TMVAEvaluator.cc
%define patchsrc5 rm -rf src/CommonTools/Utils/plugins

%define source1 git://github.com/cms-sw/cmssw.git?protocol=https&obj=%{branch}/%{gitcommit}&module=%{cvssrc}&export=%{srctree}&output=/src.tar.gz

## IMPORT cmssw-partial-build
## IMPORT scram-project-build

