checkgroups = []
subgroup_oracle =           _("Oracle Resources")

register_check_parameters(
     subgroup_applications,
    "oracle_processes",
    _("Oracle Processes"),
    Dictionary(
          help = _("Here you can override the default levels for the ORACLE Processes check. The levels "
                   "are applied on the number of used processes in percentage of the configured limit."),
          elements = [
              ( "levels",
                Tuple(
                    title = _("Levels for used processes"),
                    elements = [
                        Percentage(title = _("Warning if more than"), default_value = 70.0),
                        Percentage(title = _("Critical if more than"), default_value = 90.0)
                    ]
                )
             ),
          ],
          optional_keys = False,
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_recovery_area",
    _("Oracle Recovery Area"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels for used space (reclaimable is considered as free)"),
                     elements = [
                       Percentage(title = _("warning at"), default_value = 70.0),
                       Percentage(title = _("critical at"), default_value = 90.0),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_undostat",
    _("Oracle Undo Retention"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels for remaining undo retention"),
                     elements = [
                          Age(title = _("warning if less then"), default_value = 600),
                          Age(title = _("critical if less then"), default_value = 300),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_recovery_status",
    _("Oracle Recovery Status"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels for checkpoint time"),
                     elements = [
                          Age(title = _("warning if higher then"), default_value = 1800),
                          Age(title = _("critical if higher then"), default_value = 3600),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_rman",
    _("Oracle RMAN  Backup"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels for maximum age of an RMAN Backup"),
                     elements = [
                          Age(title = _("warning if older then"), default_value = 600),
                          Age(title = _("critical if older then"), default_value = 300),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Explicit RMAN Backups"),
        help = _("Here you can set explicit RMAN Backuptypes by defining them via SID and the Backuptype name, separated by a dot, for example <b>pengt.ARCHIVELOG</b>"),
        regex = '.+\..+',
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_sessions",
    _("Oracle Sessions"),
    Tuple(
         title = _("Number of active sessions"),
         help = _("This check monitors the current number of active sessions on Oracle"),
         elements = [
             Integer(title = _("Warning if above"),  unit = _("sessions"), default_value = 100),
             Integer(title = _("Critical if above"), unit = _("sessions"), default_value = 200),
          ],
     ),
    TextAscii(
        title = _("Database name"),
        allow_empty = False),
     None
)

register_check_parameters(
    subgroup_applications,
    "oracle_locks",
    _("Oracle Locks"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels for minimum wait time for a lock"),
                     elements = [
                          Age(title = _("warning if higher then"), default_value = 1800),
                          Age(title = _("critical if higher then"), default_value = 3600),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_longactivesessions",
    _("Oracle Long Active Sessions"),
    Dictionary(
         elements = [
             ("levels",
                 Tuple(
                     title = _("Levels of active sessions"),
                     elements = [
                          Integer(title = _("Warning if more than"), unit=_("sessions")),
                          Integer(title = _("Critical if more than"), unit=_("sessions")),
                     ]
                 )
             )
         ]
    ),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_dataguard_stats",
    _("Oracle Data-Guard Stats"),
    Dictionary(
        help = _("The Data-Guard are availible in Oracle Enterprise Edition with enabled Data-Guard. "
                 "The init.ora Parameter dg_broker_start must be TRUE for this check. The apply and "
                 "transport lag could be configured with this rule."),
        elements = [
            ( "apply_lag",
              Tuple(
                  title = _("Apply Lag"),
                  help = _( "The limit for the apply lag in v$dataguard_stats."),
                  elements = [
                      Age(title = _("Warning if above"), default_value = 10800),
                      Age(title = _("Critical if above"), default_value = 21600)])),
            ( "transport_lag",
              Tuple(
                  title = _("Transport Lag"),
                  help = _( "The limit for the transport lag in v$dataguard_stats."),
                  elements = [
                      Age(title = _("Warning if above"), default_value = 10800),
                      Age(title = _("Critical if above"), default_value = 21600)])),
                   ]),
    TextAscii(
        title = _("Database SID"),
        size = 12,
        allow_empty = False),
    "dict",
)

register_check_parameters(
    subgroup_applications,
    "oracle_jobs",
    _("Oracle Scheduler Jobs"),
    Dictionary(
        help = _("A Scheduler Job is an object in an Oracle Database which could be "
                 "compared to a cron job on unix. "
                 "This rule allows you to define checks on the size of tablespaces."),
        elements = [
            ( "run_duration",
              Tuple(
                  title = _("Maimum run duration for last execution"),
                  help = _("Here you can define an upper limit for the run duration of "
                           "last execution of the job."),
                     elements = [
                          Age(title = _("warning if higher then"), default_value = 0),
                          Age(title = _("critical if higher then"), default_value = 0),
                     ])),
            ( "disabled",
                Checkbox(
                  title = _("Disabled"),
                  label = _("Disabled is allowed"),
                  help = "Ignore the enable/disable state of the job.")),
                   ]),
    TextAscii(
        title = _("Scheduler-Job Name"),
        help = _("Here you can set explicit Scheduler-Jobs  by defining them via SID, Job-Owner "
                 "and Job-Name, separated by a dot, for example <b>TUX12C.SYS.PURGE_LOG</b>"),
        regex = '.+\..+',
        allow_empty = False),
    None
)

register_check_parameters(
    subgroup_applications,
    "asm_diskgroup",
    _("ASM Disk Group (used space and growth)"),
    Dictionary(
        elements = filesystem_elements + [
            ("req_mir_free", DropdownChoice(
             title = _("Handling for required mirror space"),
             totext = "",
             choices = [
                 ( False, _("Disregard required mirror space as free space")),
                 ( True, _("Regard required mirror space as free space")),],
             help = _("ASM calculates the free space depending on free_mb or require mirror "
                      "free space. Enable this option to set the check against require "
                      "mirror free space. This only works for normal or high redundancy Disk Groups. "))
            ),
        ],
        hidden_keys = ["flex_levels"],
    ),
    TextAscii(
        title = _("ASM Disk Group"),
        help = _("Specify the name of the ASM Disk Group "),
        allow_empty = False),
    "dict"
)
