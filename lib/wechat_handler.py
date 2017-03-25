
def send_msg_handler(msg, channel_id, sessions):
    """ when received msg from slack, post it to weixin """
    for session in sessions:
        if session.get('sid') and session.get('sid') == channel_id and session.get('wx_user'):
            session.get('wx_user').send(msg)
            return True

    print('not found mathed session')
