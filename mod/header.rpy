# header.rpy contains MAS submod header as well as Submod Updater header.
#
# This file is part of Say Something (see link below):
# https://github.com/friends-of-monika/mas-saysomething


init -990 python in mas_submod_utils:

    Submod(
        author="Friends of Monika",
        name="说点东西",
        description="让莫妮卡为你说你想听的话或摆你想看的姿势~",
        version="1.4.0",
        settings_pane="fom_saysomething_settings"
    )


init -989 python:

    if store.mas_submod_utils.isSubmodInstalled("Submod Updater Plugin"):
        store.sup_utils.SubmodUpdater(
            submod="Say Something",
            user_name="MAS-Submod-MoyuTeam",
            repository_name="mas-saysomething",
            extraction_depth=3
        )