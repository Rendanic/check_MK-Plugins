#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
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


def perfometer_check_oracle_processes(row, check_command, perf_data):
    color = { 0: "#a4f", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    return "%d" % int(perf_data[0][1]), perfometer_logarithmic(perf_data[0][1], 400, 2, color)

perfometers["check_mk-oracle_processes"]           = perfometer_check_oracle_processes


def perfometer_check_oracle_instance(row, check_command, perf_data):
    days,    rest    = divmod(int(perf_data[0][1]), 60*60*24)
    hours,   rest    = divmod(rest,   60*60)
    minutes, seconds = divmod(rest,      60)

    return "%02dd %02dh %02dm" % (days, hours, minutes), perfometer_logarithmic(perf_data[0][1], 2592000, 2, '#80F000')

perfometers["check_mk-oracle_instance"]      = perfometer_check_oracle_instance


def perfometer_check_oracle_recovery_area(row, check_command, perf_data):
    color = { 0: "#a4f", 1: "#ff2", 2: "#f22", 3: "#fa2" }[row["service_state"]]
    return "%d%%" % int(perf_data[0][1]), perfometer_logarithmic(perf_data[0][1], 400, 2, color)

perfometers["check_mk-oracle_recovery_area"]           = perfometer_check_oracle_recovery_area


def perfometer_check_oracle_undostat(row, check_command, perf_data):

    hours,    rest    = divmod(int(perf_data[2][1]), 60*60)
    minutes, seconds = divmod(rest,      60)

    return "%02dh %02dm" % (hours, minutes), perfometer_logarithmic(perf_data[2][1], 2592000, 2, '#80F000')

perfometers["check_mk-oracle_undostat"] = perfometer_check_oracle_undostat
