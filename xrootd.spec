### RPM external xrootd 20081007-0500
# Override default realversion since there is a "-" in the realversion
%define realversion 20081007-0500
Source: https://root.cern.ch/svn/root/tags/v5-18-00e/xrootd/src/%n-%{realversion}.src.tgz
Requires: openssl

%prep 
%setup -n xrootd

%build
./configure.classic --disable-krb4 --with-ssl-incdir=$OPENSSL_ROOT/include --with-ssl-libdir=$OPENSSL_ROOT/lib
make INCKRB5=-I/usr/include/et LIBKRB5=-lkrb5

%install
mkdir %i/bin
mkdir %i/lib
mkdir %i/etc
mkdir %i/utils
mkdir %i/src
cp -r bin/arch/* %i/bin
cp -r lib/arch/* %i/lib
[ $(uname) = Darwin ] &&
  for f in %i/lib/*.a; do
    ranlib $f 
  done
cp -r utils/* %i/utils
cp -r etc/* %i/etc
cp -r src/* %i/src
rm -fR %i/bin/CVS %i/lib/CVS %i/utils/CVS %i/etc/CVS %i/src/CVS %i/src/*/CVS
# Need to fix the following in the xrootd CVS
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/etc/XrdOlbMonPerf
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_PreStage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_MigrPurg
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/fs_stat
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_MonP.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_Lock.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_prep
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Stage
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_name2name.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/ooss_CAlloc.pm
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/mps_Xeq
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/utils/XrdOlbNotify.pm

perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' %i/src/XrdMon/xrdmonPrepareStats.pl

# SCRAM ToolBox toolfile
mkdir -p %i/etc/scram.d
cat << \EOF_TOOLFILE >%i/etc/scram.d/%n
<doc type=BuildSystem::ToolDoc version=1.0>
<Tool name=%n version=%v>
<lib name=XrdClient>
<lib name=XrdOuc>
<lib name=XrdNet>
<lib name=XrdSys>
<client>
 <Environment name=XROOTD_BASE default="%i"></Environment>
 <Environment name=INCLUDE default="$XROOTD_BASE/src"></Environment>
 <Environment name=LIBDIR  default="$XROOTD_BASE/lib"></Environment>
</client>
<Runtime name=PATH value="$XROOTD_BASE/bin" type=path>
<Runtime name=LD_LIBRARY_PATH value="$XROOTD_BASE/lib" type=path>
</Tool>
EOF_TOOLFILE

%post
%{relocateConfig}etc/scram.d/%n

