# TODO: Translation updated at 2022-11-01 21:13

# game/Submods/mod/topic.rpy:57
translate chinese fom_saysomething_event_entry_93e9a680:

    # m 1hub "Of course!"
    m 1hub "可以!"

# game/Submods/mod/topic.rpy:62
translate chinese fom_saysomething_event_retry_d1e010a9:

    # m 1eua "Tell me how do you want me to pose and what do you want me to say~"
    m 1eua "告诉我要做什么动作，说什么话吧~"

# game/Submods/mod/topic.rpy:64
translate chinese fom_saysomething_event_retry_25b4a108:

    # m 1eua "Tell me how do you want me to pose~"
    m 1eua "告诉我要摆什么动作吧~"

# game/Submods/mod/topic.rpy:86
translate chinese fom_saysomething_event_retry_1ba3e1e4:

    # m 1eka "Oh, okay."
    m 1eka "啊, 好吧."

# game/Submods/mod/topic.rpy:102
translate chinese fom_saysomething_event_retry_02c28211:

    # m 1esb "Alright, give me just a moment to prepare."
    m 1esb "好吧, 给我点时间准备一下."

# game/Submods/mod/topic.rpy:103
translate chinese fom_saysomething_event_retry_c6a8d13d:

    # m 2dsc "{w=0.3}.{w=0.3}.{w=0.3}.{w=0.5}{nw}"
    m 2dsc "{w=0.3}.{w=0.3}.{w=0.3}.{w=0.5}{nw}"

# game/Submods/mod/topic.rpy:113
translate chinese fom_saysomething_event_retry_474cfd2c:

    # m "[quip!q]"
    m "[quip!q]"

# game/Submods/mod/topic.rpy:124
translate chinese fom_saysomething_event_retry_861a2683:

    # m 3tua "Well? {w=0.3}Did I do it good enough?"
    m 3tua "怎么样? {w=0.3}我做的可以吗?"

# game/Submods/mod/topic.rpy:125
translate chinese fom_saysomething_event_retry_5563549d:

    # m 1hub "Hope you liked it, ahaha~"
    m 1hub "希望你喜欢, 啊哈哈~"

# game/Submods/mod/topic.rpy:132
translate chinese fom_saysomething_event_retry_132235e9:

    # m 3eub "Do you want me to [quip]?{nw}"
    if say:
        $ quip = "说些别的吗"
    else:
        $ quip = "再摆一次姿势吗"
    m 3eub "你想让我[quip]?{nw}"

# game/Submods/mod/topic.rpy:134
translate chinese fom_saysomething_event_retry_f6f65fc5:

    # m "Do you want me to [quip]?{fast}" nointeract
    m "你想让我[quip]?{fast}" nointeract

# game/Submods/mod/topic.rpy:141
translate chinese fom_saysomething_event_retry_70a9fe7e:

    # m 1hua "Okay~"
    m 1hua "好吧~"

translate chinese strings:
    old "What do you want me to say?~"
    new "想要我说什么呢?~"

translate chinese python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="fom_saysomething_event",
            category=["其它", "莫妮卡"],
            prompt="你可以说些东西吗?",
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

    addEvent(
        Event(
            persistent.event_database,
            eventlabel="fom_saysomething_event_pose",
            category=["其它", "莫妮卡"],
            prompt="你可以给我摆个pose吗?",
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