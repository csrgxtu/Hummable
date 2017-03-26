### session
for the communication between slack and wechat, we call it session. for now, session data stored in memory vars, to get information or set something, we need pass the sessions as a parameter from here to there, this makes program a little messed up. so here need a new design for session storage, i.e use sqlite3 as basic storage, and use ORM operate the storage.
