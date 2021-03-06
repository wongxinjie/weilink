## Fake-weibo
### 是什么
Fake-weibo，最初叫weilink，是我本科毕业设计，其实就是一个基于python Django框架
的一个山寨的weibo或者twitter，完成了weibo的基本功能，如发weibo/关注/粉丝管理/
私信/以及奇葩的自闭模式等等.<br/>
数据库用的是mysql， 前端用的是bootmetro。<br/>

### 长怎么样
以下是运行起来时一些模块的示例图, 也可以访问[地址](http://www.meexc.com)<br/>
* 登录页面
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/1.png)
* 首页
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/2.png)
* 主页
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/3.png)
* @提醒界面
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/4.png)
* 评论界面
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/5.png)
* 私信页面
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/6.png)
* 关注/粉丝管理页面
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/7.png)
* 信息设置
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/8.png)
* 其他设置
![](https://github.com/wongxinjie/weilink/blob/master/git_picture/9.png)

### 怎么跑起来
由于这个毕业设计最开始是跑在SAE上的，所以使用的Django版本都比较古老，所以
假设要跑起来，推荐在virtualenv中运行。<br/>
virtualenv怎么跑，google it.<br/>

### 怎么跑起来
由于这个毕业设计最开始是跑在SAE上的，所以使用的Django版本都比较古老，所以
假设要跑起来，推荐在virtualenv中运行。<br/>
virtualenv怎么跑，google it.<br/>

创建虚拟环境
```
virtualenv env  
cd env  
source bin/active  
```

创建数据库
```
mysql -uroot -p
create database weilink default charset=utf8
```

安装必要的依赖包
```
pip install -r requirements.txt
```
初始化数据库
```
python manage.py syncdb  
```
运行
```
python manager.server 8080
```

访问[localhost](http://127.0.0.1:8080)就可以看到登录界面了

