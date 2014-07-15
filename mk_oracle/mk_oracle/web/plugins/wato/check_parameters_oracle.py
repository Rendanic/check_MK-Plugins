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



# Create rules for check parameters of inventorized checks
#for subgroup, checkgroup, title, valuespec, itemspec, matchtype in checkgroups:
#    register_check_parameters(subgroup, checkgroup, title, valuespec, itemspec, matchtype)


