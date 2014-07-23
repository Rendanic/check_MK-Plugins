#!/usr/bin/python
# """
 $Id: oracle_crs.py 1035 2013-10-11 05:29:55Z tbr $
 $Date: 2013-10-11 07:29:55 +0200 (Fri, 11 Oct 2013) $

 Copyright 2013 (c) Thorsten Bruhns (tbruhns@gmx.de)

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


"""

import os, sys, subprocess

# Define the output format for this plugin.
check_mk_agentformat = 1

def GetClusterwareType():
    """
    Returncode:
    'GridInfra'  => Clusterware
    'Restart'    => Oracle Restart
    None  => No Clusterware or Oracle Restart found
    """
    # is main configfile existing?
    ocrcfgfile = '/etc/oracle/ocr.loc'

    if os.path.isfile(ocrcfgfile ) == False:
        # maincfgfile not existing
        # => Clusterware not existing!
        return None

    # ocr.loc has a configuration entry with:
    # local_only=FALSE
    # local_only=TRUE
    ocrcfg = open(ocrcfgfile , 'r')
    for line in ocrcfg:
        # search for 'local_only)'
        if line[0:11] == 'local_only=':
            # we found an entry
            # what value is there?
            localstate = line[11:].strip('\n')
            if localstate == 'FALSE':
                retcode = 'GridInfra'
                break
            elif localstate == 'TRUE':
                retcode = 'Restart'
                break
        else:
            # we found no entry
            # => no valid clusterware!
            retcode = None
    return retcode


def GetGIHome():
    olrcfgfile = '/etc/oracle/olr.loc'
    if os.path.isfile(olrcfgfile) == False:
        sys.exit(98)
    else:
        olrfile = open(olrcfgfile, 'r')
        for line in olrfile:
            if line[0:9] == 'crs_home=':
                return line[9:].rstrip('\n')


def GetCRSDstate(HAStype, ORACLE_HOME):
    """
    Checks the state of Cluster Ready Servive Daemon
    """
    crsctlexe = ORACLE_HOME + '/bin/crsctl'

    if HAStype == 'GridInfra':
        proc = subprocess.Popen([crsctlexe, 'check',  'cluster'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        okstring = 'CRS-4537:'
    elif HAStype == 'Restart':
        proc = subprocess.Popen([crsctlexe, 'check',  'has'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        okstring = 'CRS-4638:'

    procout  = proc.communicate()
    # cut 3 signs at the beginning
    procoutlist = str(procout)[2:].split('\\n')
    for line in procout:
        if line[:9] == okstring:
            return 'ONLINE'
    return False

def GetClusterVersion(HAStype, ORACLE_HOME):
    crsctlexe = ORACLE_HOME + '/bin/crsctl'

    procoutlist = ''
    if HAStype == 'GridInfra':
        proc = subprocess.Popen([crsctlexe, 'query',  'crs',  'releaseversion'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procout = proc.communicate()
        procoutlist = str(procout)[2:].split('\\n')
    elif HAStype == 'Restart':
        proc = subprocess.Popen([crsctlexe, 'query',  'has',  'releaseversion'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procout = proc.communicate()
        procoutlist = str(procout)[2:].split('\\n')
    return procoutlist[0]

def GetVotedisks(HAStype, ORACLE_HOME):
    """
    Query the votedisk information for cluster. Only usable on real Grid-Infrastructure
    crsctl query css votedisk
    """
    crsctlexe = ORACLE_HOME + '/bin/crsctl'
    GIVOTEDISKS = []

    if HAStype == 'GridInfra':
        proc = subprocess.Popen([crsctlexe, 'query',  'css',  'votedisk'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        procout = proc.communicate()
        procoutlist = str(procout)[2:].split('\\n')

        # scan for votedisks in output
        for item in procoutlist:
            if item[1] in ('1', '2', '3', '4', '5'):
                itemlist = item.split(' ')
                try:
                    GIVOTEDISKS.append([itemlist[2], itemlist[6], itemlist[5], itemlist[7]])
                except IndexError:
                    GIVOTEDISKS.append([itemlist[2], itemlist[6], itemlist[5], ''])
    return GIVOTEDISKS


def GetResources(ORACLE_HOME):
    """
    we use crs_stat for compatibility with 10g.
    => crsctl stat res is only usable from 11.2 onwards!
    """

    crsstat = ORACLE_HOME + '/bin/crs_stat'
    crsstat = ORACLE_HOME + '/bin/crsctl'
    proc = subprocess.Popen([crsstat, 'stat', 'res', '-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#    proc = subprocess.Popen([crsstat, '-f'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    procout = proc.communicate()

    procoutlist = str(procout)[2:].split('\\n')

    srvlist = []
    srvattributedict = {}

    for item in procoutlist:

        # split the line for the dictionary in itemlist
        # itemlist[0] = key
        # itemlist[1] = value
        itemlist = item.rstrip('\n').split('=', 1)
        # print itemlist

        # NAME= => New entry
        if item[0:5] == 'NAME=':
            # is the dictionary empty?
            if "NAME" in srvattributedict:
                # no, we filled the dictionary with data
                # starting a new entry, safe existing data in srvlist
                srvlist.append(srvattributedict)
            # clear an existing dictionary for next loop
            srvattributedict = {}

        # write Item in Dictionary when itemlist is >= 2 entries
        if len(itemlist) >= 2:
            valuestr = ''
            for detail in itemlist[1:]:
                valuestr = valuestr + detail + ' '
            srvattributedict[itemlist[0]] = str(valuestr.rstrip(' '))

    # De we have a filled dictionary?
    # the last entry of 'NAME=' must be safed after the loop
    if "NAME" in srvattributedict:
        # yes, we filled the dictionary with data
        srvlist.append(srvattributedict)

    return tuple(sorted(srvlist, key =lambda srvlist: srvlist['TYPE'] + srvlist['NAME']))

####################################################################
####################################################################
####################################################################

CRStype = ''
HAStype  = GetClusterwareType()

if HAStype == '':
    # we end the agent due to missing clusterware
    sys.exit(0)

print "<<<oracle_gi>>>"
print "Agent-Version $Date: 2013-10-11 07:29:55 +0200 (Fri, 11 Oct 2013) $"
ORACLE_HOME = GetGIHome()


ClusterVersion = GetClusterVersion(HAStype, ORACLE_HOME)
if HAStype == 'GridInfra':
    print "Typ Clusterware " + ClusterVersion
elif HAStype == 'Restart':
    print "Typ Restart " + ClusterVersion


if GetCRSDstate(HAStype, ORACLE_HOME) != 'ONLINE':
    # CRSD or Restart not running
    print "CRSD OFFLINE"
    sys.exit(0)
else:
    print "CRSD ONLINE"

if HAStype == 'GridInfra':
    # CRSD is online. We could get the state for Voting and Resources
    print "<<<oracle_gi_voting>>>"
    GIVotedisks = GetVotedisks(HAStype, ORACLE_HOME)
    for item in GIVotedisks:
        print str(item[0] + ' ' + item[1] + ' ' + item[3])

# We get the Resources from Clusterware
print "<<<oracle_gi_resources>>>"
print "Agent-Format " + str(check_mk_agentformat)
GIResources = GetResources(ORACLE_HOME)
for line in GIResources:
    #print sorted(line.keys())
    if line['NAME'] not in ('ora.gsd'):
        print line['NAME'] + ' ' + line['TYPE'] + ' ' + line['TARGET'] + ' ' + line['STATE']
