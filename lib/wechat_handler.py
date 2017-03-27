def send_msg_handler(msg, channel_id, sessions, slack_manager):
    """ when received msg from slack, post it to weixin """
    # parser msg into commands
    if msg.startswith('msg '):
        msg1 = msg.replace('msg ', '', 1)
        target, msg = msg1.split(' ', 1)
        send_msg_and_open_private_group(target, msg, sessions, slack_manager)
        return

    for session in sessions:
        if session.get('sid') and session.get(
                'sid') == channel_id and session.get('wx_user'):
            try:
                session.get('wx_user').send(msg)
                return True
            except:
                return False

    print('not found mathed session')


def send_msg_and_open_private_group(target, msg, sessions, slack_manager):
    for session in sessions:
        if session.get('wx_user') and session.get('wx_user').name == target:
            session.get('wx_user').send(msg)
            rtv = slack_manager.open_private_group(
                name=target, wxid=session.get('wxid'), sessions=sessions)
            slack_group = get_private_group_from_session(rtv, sessions)
            if slack_group:
                session['sid'] = rtv
                session['slack_group'] = slack_group
                return True

    return False


def get_private_group_from_session(sid, sessions):
    for session in sessions:
        if session.get('sid') and session.get('sid') == sid:
            return session.get('slack_group')
    return False
