# exchangeRateSender 澳幣匯率寄信通知器
```
部屬在 heroku 上的小玩具
每天會爬取半年內澳幣資料用 pandas 做一些基本計算，以供收信者參考
需求為澳幣低於22.0元時會寄信給使用者
```

# heroku command
```
 $ git push heroku XXXXXX:master
 # push 分支到 heroku
 $ heroku ps:scale clock=1 -a herokur_repository_name
 # 啟動 heroku 中的後台作業
 $ heroku logs --app herokur_repository_name
 # 用作查看 heroku logs
```
