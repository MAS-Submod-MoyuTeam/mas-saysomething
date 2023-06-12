# topic.rpy contains event for the 'Can you say something ...?' topic that shows
# expression/position picker and text input GUI.
#
# This file is part of Say Something (see link below):
# https://github.com/friends-of-monika/mas-saysomething

define persistent._fom_saysomething_seen_screenshot_hint = False

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

    # We'll keep looping with screen calls since we need to do Monika rendering
    # out of screen, hence why we'll keep doing it until we get 'nevermind' from
    # the player or we'll get a signal to say something.
    $ stop_picker_loop = False
    while stop_picker_loop is False:
        # Get expression from picker and add to removal list if necessary.
        $ exp = picker.get_sprite_code()
        if not _fom_saysomething.is_renpy_image_cached(exp):
            $ _fom_saysomething.IMAGE_CACHE.add_sprite(exp)

        # During the pose picking, Monika must not blink or transition from
        # winking to fully open eyes, so here we lock these transitions.
        $ set_eyes_lock(exp, True)

        # Show the GUI and await for interaction.
        call screen fom_saysomething_picker(say)

        if _return == _fom_saysomething.RETURN_CLOSE:
            # Player has changed their mind, so just stop and put Monika back.
            $ stop_picker_loop = True

            # Show buttons and quick menu if they were hidden.
            if persistent._fom_saysomething_hide_quick_buttons:
                $ _fom_saysomething.set_mas_gui_visible(True)

            # Unlock expression picker had before closing.
            $ set_eyes_lock(picker.get_sprite_code(), False)

            show monika 1eka at t11
            m 1eka "Oh, okay."

        elif _return == _fom_saysomething.RETURN_RENDER:
            # Save new expression while keeping previous; immediately lock
            # blinking on it.
            $ new_exp = picker.get_sprite_code()

            # After rendering sprite, add it to cache for further removal.
            if not _fom_saysomething.is_renpy_image_cached(new_exp):
                $ _fom_saysomething.IMAGE_CACHE.add_sprite(new_exp)

            # Unlock blinking on previous sprite.
            $ set_eyes_lock(exp, False)

            # Position or pose/expression update is requested, so do it now.
            $ renpy.show("monika " + new_exp, [picker.position], zorder=MAS_MONIKA_Z)

            # Lock blinking on new expression. NOTE: CAN ONLY BE DONE AFTER RENDERING!
            $ set_eyes_lock(new_exp, True)

            # Cleanup.
            $ del new_exp

        elif _return == _fom_saysomething.RETURN_DONE:
            # An actual text has been typed and expression is set, stop the loop
            # and show buttons if they were hidden for preview.
            $ stop_picker_loop = True
            $ _fom_saysomething.set_mas_gui_visible(True)

            # Unlock blinking on last sprite code before closing.
            $ set_eyes_lock(exp, False)

            # Pick up session items from the picker.
            # When not in session mode, session is None, so we should fall back
            # to creating an array of states with just the current state in it.
            $ picker_session = picker.session
            if picker_session is None:
                $ picker_session = [picker._save_state()]

            # Run performance, speaking or posing.
            call fom_saysomething_perform(picker_session, say, picker.pose_delay)
            $ del picker_session

            # Suggested to export current speech.
            if persistent._fom_saysomething_enable_codegen and say:
                call screen fom_saysomething_confirm_modal(_(
                    "Say Something can generate a simple topic with the speech you've just created. "
                    "Would you like to do it now?"))
                if _return: # User agreed they want to generate a topic
                    call fom_saysomething_generate

            # This is hacky, but there isn't any other way to do it with translation.
            $ quip = _("say something else") if say else _("pose for you again")
            m 3eub "Do you want me to [quip]?{nw}"

            $ _history_list.pop()
            menu:
                m "Do you want me to [quip]?{fast}"

                "Yes.":
                    jump fom_saysomething_event_retry

                "No.":
                    m 1hua "Okay~"

            # Cleanup the quip variable.
            $ del quip

    # Once done with all the speech/posing, remove the images saved in cache
    # that weren't cached before (so that we don't touch MAS sprites.)
    # Additionally, restore GUI visibility and cleanup variables.
    $ _fom_saysomething.IMAGE_CACHE.release_all()
    $ del stop_picker_loop, set_eyes_lock, say, picker
    return

label fom_saysomething_perform(session, say=True, pose_delay=None):
    # Put Monika back in center and let her say a preamble.
    show monika 1esb at t11
    m 1esb "Alright, give me just a moment to prepare."
    m 2dsc"{w=0.3}.{w=0.3}.{w=0.3}.{w=0.5}{nw}"

    if not say:
        # 'Import' set_eyes_lock.
        $ set_eyes_lock = _fom_saysomething.set_eyes_lock

        # When not in speech mode and only posing, no need to keep window open.
        window hide

    # Show or hide buttons depending on user preference.
    if persistent._fom_saysomething_hide_quick_buttons:
        $ _fom_saysomething.set_mas_gui_visible(False)

    # Show screenshot hint.
    if not persistent._fom_saysomething_seen_screenshot_hint:
        $ scr_key = _fom_saysomething.get_friendly_key("screenshot")
        if scr_key is not None:
            $ persistent._fom_saysomething_seen_screenshot_hint = True
            $ renpy.notify(_("You can take a screenshot by pressing {0}.").format(scr_key))

        # Cleanup.
        $ del scr_key

    # Memorize 5-poses for transitions.
    $ pose_5 = False

    # Ren'Py has no 'for' statement, so use 'while'.
    $ state_i = 0
    while state_i < len(session):
        $ poses, pos, text = session[state_i]
        $ state_i += 1

        # Get current expression after it was changed. Also add it to cache so
        # it can be released later, as player-made expressions may be unused in
        # the rest of MAS at all.
        $ exp = _fom_saysomething.get_sprite_code(poses)
        if not _fom_saysomething.is_renpy_image_cached(exp):
            $ _fom_saysomething.IMAGE_CACHE.add_sprite(exp)

        # Show Monika with sprite code and at set position, optionally lock
        # eyes blinking and say text. For entering and exiting 5-pose
        # apply transition.
        $ renpy.show("monika " + exp, [_fom_saysomething.POSITIONS[pos][0]], zorder=MAS_MONIKA_Z)
        if (not exp.startswith("5") and pose_5) or (exp.startswith("5") and not pose_5):
            $ renpy.with_statement(dissolve_monika)
            $ pose_5 = not pose_5

        if say:
            # Render text and ask Monika to say it.
            $ quip = _fom_saysomething_markdown.render(text)
            m "[quip]"
            $ del quip

        else:
            if not say:
                # User most likely wants Monika to hold still while posing and
                # not to blink or wink.
                $ set_eyes_lock(exp, True)

            # Pause before continuing to another expression.
            pause pose_delay

            # Unlock blinking.
            $ set_eyes_lock(exp, False)

    # Release sprites generated dynamically.
    $ _fom_saysomething.IMAGE_CACHE.release_all()

    # When in posing mode, restore dialogue window.
    if not say:
        window show

    # Anyway, recover buttons after we're done showing.
    if persistent._fom_saysomething_hide_quick_buttons:
        $ _fom_saysomething.set_mas_gui_visible(True)

    # Return Monika back to center, say post-speech phrase.
    if say and exp.startswith("5"):
        # If finished with leaning pose, apply dissolve
        show monika 3tua at t11 with dissolve_monika
    else:
        # In all the other cases just immediately change expression
        show monika 3tua at t11

    m 3tua "Well? {w=0.3}Did I do it good enough?"
    m 1hub "Hope you liked it, ahaha~"

    # Before finishing with performance, restore GUI visibility and cleanup.
    $ _fom_saysomething.set_mas_gui_visible(True)
    $ del state_i, pose_5, exp, session, poses, pos, text, set_eyes_lock
    return

# NOTE: picker instance (picker) is expected to be in the scope here.
# GENERALLY MUST NOT BE CALLED FROM ANYWHERE EXCEPT fom_saysomething_event_retry!
label fom_saysomething_generate:
    # Ask for script name in a modal window
    call screen fom_saysomething_script_name_input_modal

    # User chose 'cancel'
    if not _return:
        # If they hit cancel, they will lose their script. Need to confirm.
        call screen fom_saysomething_confirm_modal(_("Your speech script will be lost. Continue?"))

        # Confirmed, discard the script and return back.
        if _return:
            return

        # Refused to continue, jump back to input.
        else:
            jump fom_saysomething_generate

    # User entered script name and clicked okay button.
    $ script_name = _return

    # Check if script name already exists, confirm overwriting if necessary.
    if _fom_saysomething.is_script_name_exists(script_name):
        # Ask for confirmation for overwrite.
        call screen fom_saysomething_confirm_modal(_("Script with that name already exists. Do you want to overwrite it?"))

        # User did not confirm, ask again.
        if not _return:
            jump fom_saysomething_generate

    # Script name chosen, overwriting allowed if conflicted, write now.
    $ script_path = _fom_saysomething.generate_script(picker.session, script_name)
    $ renpy.notify(_("Speech saved as {0}").format(script_path))

    # Cleanup.
    $ del script_name, script_path
    return