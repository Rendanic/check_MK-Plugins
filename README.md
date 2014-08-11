Packages for Check_MK

Homepage of Check_MK: http://mathias-kettner.de/check_mk.html

# mk_oracle
This plugin was redesigned in cooperation between Mathias Kettner
and Thorsten Bruhns. mk_oracle use the new run_cached in this plugin
which makes the future development much easier then before.
The original plugin needs an agent from 1.5.5i5 onwards. This version
is a backport for Check_MK 1.2.2 or newer. It should run on older versions
as well but it is not tested on it.

## Requirements:
* Linux   RDBMS 9.2, 10.2, 11.2, XE 11.2
* AIX 5.3 RDBMS 11.2
* Check_MK Agent 1.2.2p2 or newer
* mk_oracle_dbuser.conf: ':' in password not allowed

## notable changes to original mk_oracle:
* ORACLE_SID is converted to uppercase service_name in Check_MK
* Dependency between Instancecheck and all other checks
* Instance goes CRITICAL, when Instance is not OPEN and Primary
* no need to configure sqlplus.sh anymore
* connect as sysdba is possible with mk_oracle_dbuser.conf
* Undo- and Temp-Tablespace are not notified
* Reduced number of connections to Oracle
* some checks are executed in background - reduce the execution time of agent

## new checks compared to original mk_oracle
* Instancecheck with more details about the instance
* undo Monitoring
* RMAN-Backup
* Fast-Recovery-Area
* Tablespace-Quotas
* Recovery State of a Standby Database
* Locks from v$lock
* Long Active Sessions

## known issues:
* some pnp-templates are missing
* man-pages are missing

## Version History

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

# GridInfrastructure

Thorsten Bruhns
