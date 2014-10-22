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



## notable changes to original mk_oracle:
* ORACLE_SID is converted to uppercase service_name in Check_MK
* Dependency between Instancecheck and all other checks
* Instance goes CRITICAL, when Instance is not OPEN and Primary
* connect as sysdba is possible with mk_oracle_dbuser.conf
* Undo- and Temp-Tablespace are not notified
* Reduced number of connections to Oracle
* Added req_mir_free_space and offline disks to oracle_asm_diskgroup
* Performancedata added (DB Time, DB CPU, Buffer-Cache and Library-Cache Hit-Ratio)
* some checks are executed in background - reduce the execution time of agent
* new names for ORA * Jobs, 
* Testmode added mk_oracle -t
* tnsnames.ora is replaced with addional fields in mk_oracle_dbuser.conf
* mk_oracle_dbuser.conf is removed by new variables in mk_oracle.cfg
* sqlplus.sh is removed since 2014.08.26_1.2.2p0_tbr

## new checks compared to original mk_oracle
* Instancecheck with more details about the instance
* undo Monitoring
* RMAN-Backup
* Fast-Recovery-Area
* Tablespace-Quotas
* Recovery State of a Standby Database
* Locks from v$lock
* Long Active Sessions
* Performance data

## known issues
* some pnp-templates are missing
* man-pages are missing

## Version History
* in_work: mk_oracle: bugfix for ORACLE_SID with '_'
* in_work: mk_oracle: fixed dataguard_stat availible from 10.2 onwards

* 2014.10.01_1.2.2p0_tbr: mk_oracle: Bugfix for Environments with different Oracle Versions

* 2014.09.30_1.2.2p0_tbr: mk_oracle: Oracle 9.2 is working with limited checks

* 2014.09.28_1.2.2p0_tbr: mk_oracle: added missing mk_oracle mk_oracle.aix for new ASM check

* 2014.09.27_1.2.2p0_tbr: oracle_instance added ORA +ASM Instance check
* 2014.09.27_1.2.2p0_tbr: mk_oracle: Bugfix for ASM <= 10.2 
* 2014.09.27_1.2.2p0_tbr: mk_oracle: Replaced sed -r with grep
* 2014.09.27_1.2.2p0_tbr: mk_oracle: Code Cleanup

* 2014.09.23_1.2.2p0_tbr: WATO rule for default increment
* 2014.09.23_1.2.2p0_tbr: merged all changes from mk_oracle to mk_oracle.aix

* 2014.09.17_1.2.2p0_tbr: mk_oracle: fixed broken ASYNC Sections

* 2014.09.14_1.2.2p0_tbr: oracle_performance renamed Check from ORA ORACLE_SID Perf-Data to ORA ORACLE_SID Performance. A reinventory is needed!
* 2014.09.14_1.2.2p0_tbr: oracle_performance fix for Physical Standby Databases
* 2014.09.14_1.2.2p0_tbr: oracle_instance new WATO rule for archivelog, noarchivelog, force logging, no force logging, logins and uptime
* 2014.09.14_1.2.2p0_tbr: oracle_recovery_status: Bugfix for OFFLINE datafiles
* 2014.09.14_1.2.2p0_tbr: mk_oracle: mk_oracle_dbuser.conf moved to mk_oracle.cfg
* 2014.09.14_1.2.2p0_tbr: mk_oracle: asm_diskgroup enabled by default
* 2014.09.14_1.2.2p0_tbr: mk_oracle: automatic detection of Sections for all Database Versions. No need to configure mk_oracle.cfg for that anymore.

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
* 2014.09.28_1.2.2p0_tbr: Support for Gird-Infrastructure 12.1 added

* 2014.08.29_1.2.2p0_tbr: ae03fa3 Fixed shell expansion and lower problem in mk_oracle_crs

* 0.1.0: 1st release on github

## Local Checks
# plugin_cksum

Calculates a checksum with cksum over all plugins which are found in $MK_LIBDIR/plugins.
The state is OK when plugins are found and UNKNOWN when the directory or cksum is missing.
Thorsten Bruhns
