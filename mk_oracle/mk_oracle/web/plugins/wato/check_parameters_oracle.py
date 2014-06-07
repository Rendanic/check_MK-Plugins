checkgroups = []
subgroup_oracle =           _("Oracle Resources")

checkgroups.append((
    subgroup_applications,
    "oracle_processes",
    _("Oracle Processes"),
    Dictionary(
        elements = [
            ("levels",
                Tuple(
                    title = _("Processes"),
                    elements = [
                      Float(title = _("warning at"), unit = _("%")),
                      Float(title = _("critical at"), unit = _("%"))
                    ]
                )
            )
        ]
    ),
    TextAscii(
        title = _("ORACLE SID"),
        allow_empty = True),
    "first"
))

checkgroups.append((
    subgroup_applications,
    "oracle_rman",
    _("Oracle RMAN Backup"),
    Dictionary(
        elements = [
            ("age_min",
                Tuple(
                    title = _("age of backup"),
                    elements = [
                      Float(title = _("warning older"), unit = _("minutes")),
                      Float(title = _("critical older"), unit = _("minutes"))
                    ]
                )
            )
        ]
    ),
    TextAscii(
        title = _("Database-Name"),
        allow_empty = True),
    "first"
))

checkgroups.append((
    subgroup_applications,
    "oracle_recovery_area",
    _("Oracle Recovery Area"),
    Dictionary(
        elements = [
            ("levels",
                Tuple(
                    title = _("Recovery Area"),
                    elements = [
                      Float(title = _("warning at"), unit = _("%")),
                      Float(title = _("critical at"), unit = _("%"))
                    ]
                )
            )
        ]
    ),
    TextAscii(
        title = _("ORACLE SID"),
        allow_empty = True),
    "first"
))

checkgroups.append((
    subgroup_applications,
    "oracle_ts_quotas",
    _("Oracle Tablespace Quotas"),
    Dictionary(
        elements = [
            ("levels",
                Tuple(
                    title = _("Tablespace Quotas"),
                    elements = [
                      Float(title = _("warning at"), unit = _("%")),
                      Float(title = _("critical at"), unit = _("%"))
                    ]
                )
            )
        ]
    ),
    TextAscii(
        title = _("ORACLE SID"),
        allow_empty = True),
    "first"
))

checkgroups.append((
    subgroup_storage,
    "oracle_undostat",
    _("Oracle Undostat"),
    Dictionary(
        elements = [
            ("retention",
                Tuple(
                    title = _("Undo Retention"),
                    elements = [
                      Float(title = _("warning lower"), unit = _("s")),
                      Float(title = _("critical lower"), unit = _("s"))
                    ]
                )
            )
        ]
    ),
    TextAscii(
        title = _("ORACLE SID"),
        allow_empty = True),
    "first"
))



# Create rules for check parameters of inventorized checks
for subgroup, checkgroup, title, valuespec, itemspec, matchtype in checkgroups:
    register_check_parameters(subgroup, checkgroup, title, valuespec, itemspec, matchtype)


