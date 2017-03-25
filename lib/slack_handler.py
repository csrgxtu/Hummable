
def receive_msg_handler(slack_manager, msg, Sessions):
    """ when received msg from wx, post this msg to slack """
    if msg.sender.wxid not in Sessions:
        session = dict(sid=msg.sender.wxid, sender=msg.sender)
        Sessions.append(session)

    sender = msg.sender # sender object
    text = msg.text
    msg_type = msg.type
    gid = 'G4LQR11LH'
    as_user = 'false'
    user_name = msg.sender.name + ' -- '+ msg.sender.wxid
    icon_url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_120x44dp.png'

    if msg_type is not 'Text':
        text = '[' + msg_type + '] msg type to be implemented'

    if slack_manager.send_msg_to_private_group(gid, text, as_user, user_name, icon_url):
        print('send msg from wechat ' + user_name + ' to slack ' + gid)
    else:
        print('error send msg from wechat ' + user_name + ' to slack ' + gid)
