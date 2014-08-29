Packages for Check_MK

Homepage of Check_MK: http://mathias-kettner.de/check_mk.html

# mk_oracle
This plugin was redesigned in cooperation between Mathias Kettner
and Thorsten Bruhns. mk_oracle use the new run_cached in this plugin
which makes the future development much easier then before.
The original plugin needs an agent from 1.5.5i5 onwards. This version
is a backport for Check_MK 1.2.2 or newer. It should run on older versions
as well but it is not tested on it.

## Requirements
* Linux   RDBMS 9.2, 10.2, 11.2, XE 11.2
* AIX 5.3 RDBMS 11.2
* Check_MK Agent 1.2.2p2 or newer
* mk_oracle_dbuser.conf: ':' in password not allowed

## notable changes to original mk_oracle:
* ORACLE_SID is converted to uppercase service_name in Check_MK
* Dependency between Instancecheck and all other checks
* Instance goes CRITICAL, when Instance is not OPEN and Primary
* sqlplus.sh is removed since 2014.08.26_1.2.2p0_tbr
* tnsnames.ora is replaced with addional fields in mk_oracle_dbuser.conf
* connect as sysdba is possible with mk_oracle_dbuser.conf
* Undo- and Temp-Tablespace are not notified
* Reduced number of connections to Oracle
* Added req_mir_free_space and offline disks to oracle_asm_diskgroup
* Performancedata added (DB Time, DB CPU, Buffer-Cache and Library-Cache Hit-Ratio)
* some checks are executed in background - reduce the execution time of agent
* new names for ORA * Jobs, 
* Testmode added mk_oracle -t

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


# 2014.08.29_1.2.2p0_tbr: added missing changes for removing tnsnames.ora requirements
# 2014.08.26_1.2.2p0_tbr: New Version numbering due to irritations between Check_MK and this plugin (timestamp of creation the mkp + compatible against Check_MK-Version + _tbr)
# 2014.08.26_1.2.2p0_tbr: added owner in oracle_jobs service, added req_mir_free_space and offline disk in oracle_asm_diskgroup
# 2014.08.26_1.2.2p0_tbr: sqlplus.sh is not required anymore, tnsnames.ora is replaced with more fields in mk_oracle_dbusers.conf
# 2014.08.26_1.2.2p0_tbr: oracle_performance gets some performance data from Oracle
# 2014.08.26_1.2.2p0_tbr: Testmode added: mk_oracle -t
# 1.2.3: Bugfix wrong order of values in default parameters in oracle_recovery_status
# 1.2.2: Bugfix sqlplus.sh, wallet is usable again
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
* Linux   Grid-Infrastructure or Oracle Restart 11.2
* Check_MK Agent 1.2.2p2 or newer

## Version History
* 0.1.0: 1st release on github

## Local Checks
# plugin_cksum

Calculates a checksum with cksum over all plugins which are found in $MK_LIBDIR/plugins.
The state is OK when plugins are found and UNKNOWN when the directory or cksum is missing.
Thorsten Bruhns
