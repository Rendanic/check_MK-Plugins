#!/bin/sh
# +------------------------------------------------------------------+
# |             ____ _               _        __  __ _  __           |
# |            / ___| |__   ___  ___| | __   |  \/  | |/ /           |
# |           | |   | '_ \ / _ \/ __| |/ /   | |\/| | ' /            |
# |           | |___| | | |  __/ (__|   <    | |  | | . \            |
# |            \____|_| |_|\___|\___|_|\_\___|_|  |_|_|\_\           |
# |                                                                  |
# | Copyright Mathias Kettner 2013             mk@mathias-kettner.de |
# +------------------------------------------------------------------+
#
# This file is part of Check_MK.
# The official homepage is at http://mathias-kettner.de/check_mk.
#
# check_mk is free software;  you can redistribute it and/or modify it
# under the  terms of the  GNU General Public License  as published by
# the Free Software Foundation in version 2.  check_mk is  distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;  with-
# out even the implied warranty of  MERCHANTABILITY  or  FITNESS FOR A
# PARTICULAR PURPOSE. See the  GNU General Public License for more de-
# ails.  You should have  received  a copy of the  GNU  General Public
# License along with GNU Make; see the file  COPYING.  If  not,  write
# to the Free Software Foundation, Inc., 51 Franklin St,  Fifth Floor,
# Boston, MA 02110-1301 USA.

# support for clusterware and connect as sysdba added by:
# Thorsten Bruhns <thorsten.bruhns@opitz-consulting.com>
#
# The script could use different ways for connecting to Oracle:
# - EZCONNECT-Syntax
#   Default when no tnsnames.ora is existing
# - tnsnames.ora
#   tnsnames must have an entry for the ORACLE_SID
# - without wallet
#   only working in combination with tnsnames.ora
#   could be used to connect as sysdba/sysoper to a database
#   a configuration file is needed: MK_CONFDIR/mk_oracle_dbuser.conf
#   ORACLE_SID:Username:Password:<optional SYSDBA/SYSOPER>
#
# How to create the wallet?
# mkstore -wrl /etc/check_mk/oracle_wallet -create
# mkstore -wrl /etc/check_mk/oracle_wallet --createEntry trac1 dbsnmp dbsnmp

# EXAMPLE

# This script is called by the Check_MK ORACLE plugin in order to 
# execute an SQL query. 


# The script will get the query on stdin and shall output the
# result on stdout. Error messages goes to stderr.

ORACLE_SID=$1
if [ -z "$ORACLE_SID" ] ; then
    echo "Usage: $0 ORACLE_SID" >&2
    exit 1
fi

ORACLE_USERCONF=${MK_CONFDIR}/mk_oracle_dbuser.conf

if [ -f /etc/oratab ]
then
	ORATAB=/etc/oratab
elif [ -f /var/opt/oracle/oratab ]
then
	ORATAB=/var/opt/oracle//oratab
fi

ORACLE_HOME=$(cat ${ORATAB} | grep "^"${ORACLE_SID}":" | cut -d":" -f2)
if [ -z $ORACLE_HOME ] ; then
    # cut last number from SID for Oracle RAC to find entry in oratab
    ORACLE_SID_SHORT=$(echo $ORACLE_SID | sed "s/[0-9]$//")
    ORACLE_HOME=$(cat ${ORATAB} | grep "^"${ORACLE_SID_SHORT}":" | cut -d":" -f2)
fi

if [ ! -d ${ORACLE_HOME:-"not_found"} ] ; then
    echo "ORA-99999 ORACLE_HOME for ORACLE_SID="$ORACLE_SID" not found or not existing!"
    exit 1
fi

export TNS_ADMIN=/etc/check_mk

# check for sqlnet.ora
# => exit 1 when sqlnet.ora does not exist
test -f ${TNS_ADMIN}/sqlnet.ora || ( echo "ORA-99998 Couldn't find "${TNS_ADMIN}/sqlnet.ora ; exit 1)

# Check for an existing tnsnames.ora
# yes => Use an alias for connecting to the database
# no  => Use EZCONNECT-Syntax with localhost/<ORACLE_SID>
# This is needed in environment where localhost couldn't be used for connecting
# to Oracle.

if [ -f ${TNS_ADMIN}/tnsnames.ora ]
then
	# Use TNSNAMES.ORA
	connectstring=${ORACLE_SID}
	${ORACLE_HOME}/bin/tnsping ${ORACLE_SID} > /dev/null 2>&1 
	if [ ${?} -ne 0 ]
	then
		# tnsping not possible
		# => Connect to Oracle won't work!
		echo "ORA-99999 tnsping failed for "${ORACLE_SID}
		exit 1
        else
            TNSALIAS=$ORACLE_SID
	fi
fi

# we have a configuration file for SID:USER:PASSWORD?
if [ ! -f ${ORACLE_USERCONF} ] ; then
    # use EZCONNECT
    DBUSER=""
    DBPASSWORD=""
    TNSALIAS=localhost/$ORACLE_SID
else
    # connect as sysdba/sysoper?
    DBSYSCONNECT=$(echo ${dbconfline} | cut -d":" -f4)
    if [ ${DBSYSCONNECT} ] ; then
        assysdbaconnect=" as "${DBSYSCONNECT}
    fi

    dbconfline=$(cat ${ORACLE_USERCONF} | grep "^"${ORACLE_SID}":")
    if [ ! ${dbconfline} ] ; then
        # no configuration for ORACLE_SID found
        # => use the wallet with tnsnames.ora!
        DBUSER=""
        DBPASSWORD=""
        TNSALIAS=localhost/$ORACLE_SID
    else
        # connect as sysdba/sysoper?
        DBSYSCONNECT=$(echo ${dbconfline} | cut -d":" -f4)
        if [ ${DBSYSCONNECT} ] ; then
            assysdbaconnect=" as "${DBSYSCONNECT}
        fi

        DBUSER=$(echo ${dbconfline} | cut -d":" -f2)
        DBPASSWORD=$(echo ${dbconfline} | cut -d":" -f3)
        # DBUSER = '/'?
        # => ignore DBPASSWORD and use the wallet with tnsnames.ora
        if [ ${DBUSER} = '/' ] ; then
            DBUSER=""
            DBPASSWORD=""
            TNSALIAS=localhost/$ORACLE_SID
        fi
    fi
fi

DBCONNECT=${DBUSER}/"${DBPASSWORD}@"${TNSALIAS}${assysdbaconnect}

SQLPLUS=${ORACLE_HOME}/bin/sqlplus
if [ ! -x ${SQLPLUS} ]
then
        echo "sqlplus not found or ORACLE_HOME wrong! "
        echo "SQLPLUS="${SQLPLUS}
        exit 1
fi

export ORACLE_HOME
export ORACLE_SID

${SQLPLUS} -L -s ${DBCONNECT}

