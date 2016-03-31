checkgroups = []
subgroup_oracle =           _("Oracle Resources")

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

