# topic.rpy contains event for the 'Can you say something ...?' topic that shows
# expression/position picker and text input GUI.
#
# This file is part of Say Something (see link below):
# https://github.com/friends-of-monika/mas-saysomething


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="fom_saysomething_event",
            category=["misc", "monika"],
            prompt="Can you say something for me?",
            pool=True,
            unlocked=True,

            # Allow this event to be bookmarked since it isn't prefixed with
            # mas_ or monika_.
            rules={"bookmark_rule": mas_bookmarks_derand.WHITELIST}
        ),
        code="EVE",

        # Prevent this topic from restarting with 'Now, where was I...' on crash.
        restartBlacklist=True
    )

label fom_saysomething_event:
    call fom_saysomething_event_entry(say=True)
    return _return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="fom_saysomething_event_pose",
            category=["misc", "monika"],
            prompt="Can you pose for me?",
            pool=True,
            unlocked=True,

            # Allow this event to be bookmarked since it isn't prefixed with
            # mas_ or monika_.
            rules={"bookmark_rule": mas_bookmarks_derand.WHITELIST}
        ),
        code="EVE",

        # Prevent this topic from restarting with 'Now, where was I...' on crash.
        restartBlacklist=True
    )

label fom_saysomething_event_pose:
    call fom_saysomething_event_entry(say=False)
    return _return

label fom_saysomething_event_entry(say=True):
    m 1hub "Of course!"

label fom_saysomething_event_retry:
    # Need a fallthrough here so we can jump back here on retry.
    if say:
        m 1eua "Tell me how do you want me to pose and what do you want me to say~"
    else:
        m 1eua "Tell me how do you want me to pose~"

    # Create new Picker and store it locally.
    $ _fom_saysomething.picker = _fom_saysomething.Picker()
    $ picker = _fom_saysomething.picker

    # If player wants speech/session mode by default, enable it now.
    if persistent._fom_saysomething_speech_mode_default:
        $ picker.enable_session_mode()

    # 'Import' set_eyes_lock.
    $ set_eyes_lock = _fom_saysomething.set_eyes_lock

    # Set of expressions to remove from Ren'Py image cache after we're done.
    $ created_expressions = set()

    # We'll keep looping with screen calls since we need to do Monika rendering
    # out of screen, hence why we'll keep doing it until we get 'nevermind' from
    # the player or we'll get a signal to say something.
    $ stop_picker_loop = False
    while stop_picker_loop is False:
        # Get expression from picker.
        $ exp = picker.get_sprite_code()

        # If there were too many images saved in cache, free them all.
        if len(created_expressions) > 200:
            $ _fom_saysomething.remove_renpy_images_bulk(created_expressions)

        # If the spritecode isn't in cache already, mark it for removal.
        if _fom_saysomething.is_renpy_image_cached(exp):
            $ created_expressions.add(exp)

        # During the pose picking, Monika must not blink or transition from
        # winking to fully open eyes, so here we lock these transitions.
        if not persistent._fom_saysomething_allow_winking:
            $ set_eyes_lock(exp, True)

        # Show the GUI and await for interaction.
        $ _fom_saysomething.posing = True
        call screen fom_saysomething_picker(say)
        $ _fom_saysomething.posing = False

        if _return == _fom_saysomething.RETURN_CLOSE:
            # Player has changed their mind, so just stop and put Monika back.
            $ stop_picker_loop = True

            # Show buttons and quick menu if they were hidden.
            if persistent._fom_saysomething_hide_quick_buttons:
                call fom_saysomething_event_buttons(_show=True)

            # Unlock expression picker had before closing.
            $ set_eyes_lock(picker.get_sprite_code(), False)

            show monika 1eka at t11
            m 1eka "Oh, okay."

        elif _return == _fom_saysomething.RETURN_RENDER:
            $ new_exp = picker.get_sprite_code()

            # Before rendering, check if the sprite that was already cached
            # before render in pose picker; mark for removal later.
            if _fom_saysomething.is_renpy_image_cached(exp):
                $ created_expressions.add(exp)

            # Position or pose/expression update is requested, so do it now.
            $ renpy.show("monika " + new_exp, [picker.position], zorder=MAS_MONIKA_Z)

            # Lock winking/blinking on the new image.
            if not persistent._fom_saysomething_allow_winking:
                # Lock new expression.
                $ set_eyes_lock(new_exp, True)

            # Once out of GUI, unlock the winking/blinking on the previous
            # sprite. This would also unlock expression locked when in GUI.
            $ set_eyes_lock(exp, False)

        elif _return == _fom_saysomething.RETURN_DONE:
            # An actual text has been typed and expression is set, stop the loop
            # and show buttons if they were hidden for preview.
            $ stop_picker_loop = True
            call fom_saysomething_event_buttons(_show=True)

            # Here it's safe to just take a sprite code as it's already
            # rendered and respective image is loaded into memory.
            $ set_eyes_lock(picker.get_sprite_code(), False)

            show monika 1esb at t11
            m 1esb "Alright, give me just a moment to prepare."
            m 2dsc"{w=0.3}.{w=0.3}.{w=0.3}.{w=0.5}{nw}"

            # Show or hide buttons depending on user preference.
            if persistent._fom_saysomething_hide_quick_buttons:
                call fom_saysomething_event_buttons(_show=False)

            # Pick up session items from the picker.
            # When not in session mode, session is None, so we should fall back
            # to creating an array of states with just the current state in it.
            $ picker_session = picker.session
            if picker_session is None:
                $ picker_session = [picker._save_state()]

            # Ren'Py has no 'for' statement, so use 'while'.
            $ state_i = 0
            while state_i < len(picker_session):
                $ picker._load_state(picker_session[state_i])
                $ state_i += 1

                # Show screenshot hint.
                if not persistent._fom_saysomething_seen_screenshot_hint:
                    $ scr_key = _fom_saysomething.get_screenshot_key()
                    if scr_key is not None:
                        $ persistent._fom_saysomething_seen_screenshot_hint = True
                        $ renpy.notify(_("You can take a screenshot by pressing {0}.").format(scr_key))
                    $ del scr_key

                # Get current expression after it was changed.
                $ exp = picker.get_sprite_code()

                # Lock winking/blinking for the current sprite code.
                if not persistent._fom_saysomething_allow_winking:
                    $ set_eyes_lock(exp, True)

                # Set flag as posing.
                $ _fom_saysomething.posing = True

                # Show Monika with sprite code and at set position, optionally lock
                # eyes blinking and say text. For entering and exiting 5-pose
                # apply transition.
                $ exp_5 = False
                $ renpy.show("monika " + exp, [picker.position], zorder=MAS_MONIKA_Z)
                if exp.startswith("5") or exp_5:
                    $ renpy.with_statement(dissolve_monika)
                    $ exp_5 = not exp_5

                # Finally, say text or show pose for 5 seconds.
                if say:
                    $ quip = picker.text
                    if persistent._fom_saysomething_markdown_enabled:
                        $ quip = _fom_saysomething_markdown.render(quip)
                    m "[quip!q]"
                else:
                    window hide
                    pause picker.pose_delay
                    window show

            # Cleanup.
            $ del state_i, picker_session

            # No longer posing.
            $ _fom_saysomething.posing = False

            # Unlock winking/blinking.
            $ set_eyes_lock(exp, False)

            # Anyway, recover buttons after we're done showing.
            if persistent._fom_saysomething_hide_quick_buttons:
                call fom_saysomething_event_buttons(_show=True)

            show monika 3tua at t11
            m 3tua "Well? {w=0.3}Did I do it good enough?"
            m 1hub "Hope you liked it, ahaha~"

            if say:
                $ quip = _("say something else")
            else:
                $ quip = _("pose for you again")

            m 3eub "Do you want me to [quip]?{nw}"
            $ _history_list.pop()
            menu:
                m "Do you want me to [quip]?{fast}"

                "Yes.":
                    jump fom_saysomething_event_retry

                "No.":
                    m 1hua "Okay~"

    # Once done with all the speech/posing, remove the images saved in cache
    # that weren't cached before (so that we don't touch MAS sprites.)
    $ _fom_saysomething.remove_renpy_images_bulk(created_expressions)
    $ del created_expressions

    call fom_saysomething_event_buttons(_show=True)
    return

label fom_saysomething_event_buttons(_show=True):
    # Here we're recovering (since show=True when not called) buttons after
    # player chose to hide them.
    $ quick_menu = _show
    if _show:
        $ HKBShowButtons()
    else:
        $ HKBHideButtons()
    return