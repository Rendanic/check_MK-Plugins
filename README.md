Packages for Check_MK

Homepage of Check_MK: http://mathias-kettner.de/check_mk.html

# mk_oracle
This plugin was redesigned in cooperation between Mathias Kettner
and Thorsten Bruhns. mk_oracle use the new run_cached in this plugin
which makes the future development much easier then before.
The original plugin needs an agent from 1.2.5i5 onwards. This version
is a backport for Check_MK 1.2.2 or newer. It should run on older versions
as well but it is only tested on 1.2.5i5. 
I will stop the backporting for this plugin with the next production 
version (1.2.6) of Check_MK.

## Requirements
* Linux   RDBMS 9.2, 10.2, 11.1, 11.2, XE 11.2, 12.1
* AIX 5.3 RDBMS 11.2
* ASM: 10.2, 11.1, 11.2, 12.1 
* Check_MK Agent 1.2.2p2 or newer

## How to configure the plugin
The configuration is very simple since 2014.09.14_1.2.2p0_tbr.
The usage of an Oracle wallet is not documented here.

### Copy sqlnet.ora to $MK_CONFDIR. 

This file is needed for the Oracle Client to prevent unwanted diagnostic 
data to the homedirectory of root. An Oracle wallet also needs the
sqlnet.ora.

### Configure a Database User
This depends on the instance_type.
#### Normal Instance:

    sqlplus / as sysdba
    create user check_mk identified by monitoring;
    grant connect, select_catalog_role to check_mk;

#### ASM Instance

    sqlplus / as sysasm
    create user check_mk identified by monitoring;
    grant sysdba to check_mk;

Normaly the sysdba is not supported for ASM anymore. This is still working 
under 11.2 and 12.1 and has the advantage that check_mk is not able to stop
the Instance but can read the needed data from the Instance.

Do not use special characters like '$&" or spaces in passwords.

### Configure $MK_CONFDIR/mk_oracle.cfg

The mk_oracle.cfg has some options.

    ASMUSER='user:password:sysdba'
    DBUSER='user:password:sysdba/sysoper:hostname:port'
    DBUSER_<ORACLE_SID>='user:password:sysdba/sysoper:hostname:port'

DBUSER= is used as a default for all normal Database Instances. This can be 
overwritten by an individual configuration with DBUSER_<ORACLE_SID>.

* sysdba/sysoper is empty
* hostname localhost
* port 1521

    ASMUSER='user:password:sysdba'

Example:

    ASMUSER="asmsnmp:asmsnmp:sysdba"
    DBUSER="check_mk:monitoring"
    DBUSER_tux="check_mk:monitoring:sysdba"

### Test the plugin

Login as root

    export MK_CONFDIR=/etc/check_mk
    /usr/lib/check_mk_agent/plugins/mk_oracle -t

## known issues
* some pnp-templates are missing
* man-pages are missing

## Version History
* 2015.03.31_1.2.2p0_tbr: oracle_recovery_status: Bugfix for checkpoints in the future
* 2015.03.31_1.2.2p0_tbr: added a missing bugifx for #1903
* 2015.03.27_1.2.2p0_tbr: #1903 mk_oracle: Remote Monitoring of Oracle Databases
* 2015.03.27_1.2.2p0_tbr: mk_oracle: Bugfix for oracle session environment and ASM Instances
* 2015.03.20_1.2.2p0_tbr: oracle_tablespace: removed configuration variable from check oracle_tablespaces_check_default_increment
* 2015.03.20_1.2.2p0_tbr: oracle_tablespace: copied code from #1920 (reserved space for root) - no new functions in check!
* 2015.03.20_1.2.2p0_tbr: oracle_asm_diskgroup: copied code from #1920 (reserved space for root) - no new functions in check!
* 2015.03.20_1.2.2p0_tbr: #1902 mk_oracle: Performance hint for RMAN checks
* 2015.03.20_1.2.2p0_tbr: #1901 mk_oracle: IGNORE_DB_NAME for special environments
* 2015.03.20_1.2.2p0_tbr: #1900 mk_oracle: added oracle session environment
* 2015.03.20_1.2.2p0_tbr: #1899 FIX mk_oracle: backport of werk 1564 from agent
* 2015.01.19_1.2.2p0_tbr: oracle_dataguard_stats: Bugfix for 'params_value' referenced before assignment
* 2015.01.19_1.2.2p0_tbr: oracle_undostat: Code cleanup for UNKNOWN state marker
* 2015.01.14_1.2.2p0_tbr: mk_oracle: Added missing rules for oracle_jobs and oracle_undostat
* 2015.01.12_1.2.2p0_tbr: oracle_rman: Check for new format from agent
* 2015.01.12_1.2.2p0_tbr: oracle_rman: new SQL for FULL and INCR Backups
* 2015.01.12_1.2.2p0_tbr: oracle_jobs: new SQL for jobs without log information
* 2015.01.12_1.2.2p0_tbr: oracle_jobs: added rules for missing job and missing log information
* 2015.01.12_1.2.2p0_tbr: #1826 oracle_dataguard_stats: New rule for apply_lag_min, removed default rule
* 2015.01.12_1.2.2p0_tbr: #1825 oracle_recovery_status: backupcheck for user managed backups
* 2015.01.12_1.2.2p0_tbr: #1822 oracle_undostat: rule for non space error count
* 2014.12.29_1.2.2p0_tbr: moved sqlnet.ora to cfg_samples
* 2014.12.29_1.2.2p0_tbr: #1821 FIX mk_oracle: changed connection to dedicated server mode
* 2014.12.29_1.2.2p0_tbr: #1824 FIX oracle_recovery_status: removed default values from Check
* 2014.12.29_1.2.2p0_tbr: #1821 FIX mk_oracle: changed connection to dedicated server mode
* 2014.12.29_1.2.2p0_tbr: #1391 FIX oracle_instance: New function for Primary Database not OPEN
* 2014.12.29_1.2.2p0_tbr: #1726 Move variable data of Linux/UNIX agents to /var/lib/check_mk_agent
* 2014.12.05_1.2.2p0_tbr: #1390 FIX mk_oracle: better detection of RMAN Archivelog Backups
* 2014.11.25_1.2.2p0_tbr: #1511 FIX oracle_jobs: avoid broken checks, make compatible with old version
* 2014.11.24_1.2.2p0_tbr: #1388 FIX oracle_asm_diskgroup: fixed wrong calculation of free space in NORMAL/HIGH redundancy Disk Groups
* 2014.11.12_1.2.2p0_tbr: #1824 FIX oracle_recovery_status: removed default values from Check
* 2014.11.04_1.2.2p0_tbr: #1389 FIX oracle_rman: detect failed jobs
* 2014.10.28_1.2.2p0_tbr: bugfix for ORACLE_SID with '_'
* 2014.10.28_1.2.2p0_tbr: fixed dataguard_stat availible from 10.2 onwards
* 2014.10.28_1.2.2p0_tbr: fixed missing executes of sql for 10.1
* 2014.10.28_1.2.2p0_tbr: fixed forever running Jobs in oracle_jobs
* 2014.10.28_1.2.2p0_tbr: added new Instance MGMTDB for Oracle 12.1.0.2
* 2014.10.01_1.2.2p0_tbr: Bugfix for Environments with different Oracle Versions
* 2014.09.30_1.2.2p0_tbr: Oracle 9.2 is working with limited checks
* 2014.09.28_1.2.2p0_tbr: added missing mk_oracle mk_oracle.aix for new ASM check
* 2014.09.27_1.2.2p0_tbr: oracle_instance added ORA +ASM Instance check
* 2014.09.27_1.2.2p0_tbr: Bugfix for ASM <= 10.2 
* 2014.09.27_1.2.2p0_tbr: Replaced sed -r with grep
* 2014.09.27_1.2.2p0_tbr: Code Cleanup
* 2014.09.23_1.2.2p0_tbr: WATO rule for default increment
* 2014.09.23_1.2.2p0_tbr: merged all changes from mk_oracle to mk_oracle.aix
* 2014.09.17_1.2.2p0_tbr: fixed broken ASYNC Sections
* 2014.09.14_1.2.2p0_tbr: oracle_performance renamed Check from ORA ORACLE_SID Perf-Data to ORA ORACLE_SID Performance. A reinventory is needed!
* 2014.09.14_1.2.2p0_tbr: oracle_performance fix for Physical Standby Databases
* 2014.09.14_1.2.2p0_tbr: oracle_instance new WATO rule for archivelog, noarchivelog, force logging, no force logging, logins and uptime
* 2014.09.14_1.2.2p0_tbr: oracle_recovery_status: Bugfix for OFFLINE datafiles
* 2014.09.14_1.2.2p0_tbr: mk_oracle_dbuser.conf moved to mk_oracle.cfg
* 2014.09.14_1.2.2p0_tbr: asm_diskgroup enabled by default
* 2014.09.14_1.2.2p0_tbr: automatic detection of Sections for all Database Versions. No need to configure mk_oracle.cfg for that anymore.
* 2014.08.29_1.2.2p0_tbr: added missing changes for removing tnsnames.ora requirements
* 2014.08.26_1.2.2p0_tbr: New Version numbering due to irritations between Check_MK and this plugin (timestamp of creation the mkp + compatible against Check_MK-Version + _tbr)
* 2014.08.26_1.2.2p0_tbr: added owner in oracle_jobs service, added req_mir_free_space and offline disk in oracle_asm_diskgroup
* 2014.08.26_1.2.2p0_tbr: sqlplus.sh is not required anymore, tnsnames.ora is replaced with more fields in mk_oracle_dbusers.conf
* 2014.08.26_1.2.2p0_tbr: oracle_performance gets some performance data from Oracle
* 2014.08.26_1.2.2p0_tbr: Testmode added: mk_oracle -t
* 1.2.3: Bugfix wrong order of values in default parameters in oracle_recovery_status
* 1.2.2: Bugfix sqlplus.sh, wallet is usable again
* 1.2.0: New oracle_locks, oracle_longactivesessions Bugfix oracle_job, oracle_recovery_status. More feautures in sqlplus.sh
* 1.1.1: Bugfix oracle_instance & oracle_jobs, some perfometers
* 1.1.0: New Recovery State for Standby Databases
* 1.0.0: Redesign of whole plugin
* 0.7.5: Bugfix UNKNOWN services every 10 minutes from mk_oracle 
* 0.7.4: Bugfix removed nasty debug print from oracle_instance
* 0.7.3: Bugfix in oracle_instance
* 0.7.2: Bugfix sqlplus.sh for EZCONNECT
* 0.7.1: 1st big release on github

# mk_oracle_crs
This plugin is used to check an Oracle Grid-Infrastructure or Oracle Restart.

## Requirements
* Linux   Grid-Infrastructure or Oracle Restart 11.2 + 12.1, Oracle CRS 10.2 + 11.1
* Check_MK Agent 1.2.2p2 or newer

## Version History
* 2015.01.16.1.2.2p0_tbr: Plugin compatibility against CRS 10.2 and 11.1
* 2014.11.06.1.2.2p0_tbr: fix for Pending Services in CRS or GI Environments
* 2014.09.28_1.2.2p0_tbr: Support for Gird-Infrastructure 12.1 added
* 2014.09.28_1.2.2p0_tbr: Support for Gird-Infrastructure 12.1 added

* 2014.08.29_1.2.2p0_tbr: ae03fa3 Fixed shell expansion and lower problem in mk_oracle_crs

* 0.1.0: 1st release on github

## Local Checks
# plugin_cksum

Calculates a checksum with cksum over all plugins which are found in $MK_LIBDIR/plugins.
The state is OK when plugins are found and UNKNOWN when the directory or cksum is missing.
Thorsten Bruhns
