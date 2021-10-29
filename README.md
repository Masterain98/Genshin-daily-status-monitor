# Genshin-daily-status-monitor
监控原神树脂和派遣任务状态并通过Telegram推送消息

## 监控项目

- 原粹树脂
  - 当前数量
  - 剩余恢复时间
  - 预计恢复完成时间
- 每日任务
  - 完成状态
- 周本
  - 树脂消耗减半机会剩余次数
- 派遣任务
  - 当前状态
  - 剩余时间
  - 预计派遣任务完成时间

## 为什么写这个

1. 原神对PC端玩家没有一个好用的消息推送设计
   1. 考虑到在PC端发出派遣任务后，再使用移动端登录后，派遣完成的推送会被发送到移动端，可以推测该数据可能被临时地被存储在本地。也许未来可以研究一下原神PC端的注册表信息中是否有保存这一信息。
2. 米游社实时便签功能不会推送重要消息
3. 米游社的主页面在海外访问缓慢，且有间歇性无法访问的情况

## 使用方法

1. 在米游社应用中开启帐号的```实时便签```功能
2. 在```config/config.json``` 中填写
   1. 原神游戏内UID
   2. Telegram BOT的Token
   3. Telegram消息接受者的ID (userID)
3. 在```config/cookie.txt``` 中粘贴你的米游社cookie
4. (可选) 在```core/setting.py```中修改```default_roll_polling_time```的值已修改默认的状态轮询间隔时间
   1. 默认值为```3600``` ，即60分钟
   2. 程序会在当前查询结果的```原粹树脂剩余回复时间```，```最短派遣任务完成剩余时间```和```default_roll_polling_time```三个值之间取最小值作为下一次轮询间隔时间
5. 运行```main.py```

## 代码参考

- 米游社HTTP Header的设置：
  - [Womsxd/YuanShen_User_Info][1]



[1]:https://github.com/Womsxd/YuanShen_User_Info
