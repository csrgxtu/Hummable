
def send_msg_handler(msg, channel_id, wx_sessions):
    """ when received msg from slack, post it to weixin """
    # split wxid msg
    if ' ' in msg:
        wxid, text = msg.split(' ', 1)
        # query WechatSessions
        for session in wx_sessions:
            if wxid == session.get('sid'):
                sender = session.get('sender')
                sender.send(text)
                break
    else:
        print(msg)
