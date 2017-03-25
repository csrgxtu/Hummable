
def send_msg_handler(msg, Sessions):
    """ when received msg from slack, post it to weixin """
    # split wxid msg
    if ' ' in msg:
        wxid, text = msg.split(' ', 1)
        # query WechatSessions
        for session in Sessions:
            if wxid == session.get('sid'):
                sender = session.get('sender')
                sender.send(text)
    else:
        print(msg)
