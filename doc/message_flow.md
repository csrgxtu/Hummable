1, msg come from wechat_manager to mq topic

```json

{
  "type": "",
  "src_id": "",
  "src_name": "",
  "content": "",
}
```
* wechat manager listen on msg event
* put msg in mq topic slack_in with upper json format

2, msg come from mq topic to slack_manager

* slack_manager subscribed to mq topic slack in
* once received a msg, open a group in the Slack
* send the msg content to the Slack in the group you just created
* store this slack and wechat conversation identifier in following format


```json
{
  "type": "",
  "slack_group_id": "",
  "companion_id": ""
}
```

3, you type a msg in Slack
4, slack_manager received a msg event and put the msg into mq topic slack_out

* according the group id, find companion_id
* compose a msg and send to topic slack_out

5, wechat manager received the upper msg from topic slack_out
