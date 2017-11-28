# myblog项目安装方法
鉴于有同学询问我安装的问题，特写此文详细说一下项目安装方法，希望大家能一起多多交流～  
因为此项目遵循了《Flask web开发》一书的项目结构，所以看过这本书的同学，自然会使用配置了。  
项目中还涉及的很多廖大教程里没有的东西（数据库迁移等），所以想详细了解的话可以去看看这本书，我这里只简单写一下如何最快配置然后让项目跑起来。  

如果对我的小项目还满意的话，请star右上角以资鼓励哈，谢谢～！  
项目源码[请见]()   
## 本地环境搭建（windows）  
### 1、安装`virtualenv`虚拟环境  
为了防止本项目安装的扩展包与你的本地包出现版本冲突等情况，强烈建议将本项目安装到虚拟环境中。   
使用pip安装：  
```
pip install virtualenv
```
在项目目录下，初始化虚拟环境：  
```
virtualenv venv
```
初始化完毕后，启动virtualenv的Shell环境：  
```
venv\Scripts\activate
```
命令行输入界面左侧提示符变成`<venv>`说明已进入Shell。  
退出可直接输入```deactivate```即可恢复正常命令行。 
### 2、安装扩展包
在项目文件根目录下有requestments.txt需求文件，保存了项目所需的扩展包  
启动虚拟环境Shell，用pip一键安装：  
```
pip install -r requirements.txt
```
可以看到`pip`会自动将包安装完毕。  
### 3、配置文件  
项目根目录下的`config.py`是我本地开发环境的配置，还请根据自己的本地环境重新配置。  
**a、mysql配置**  
config.py中的类，分别用于开发，生产，测试三种环境，其中都涉及到mysql的连接。  
配置mysql需要写URI，以下URI请根据实际情况做修改。  
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost:3306/database'
```
`user`mysql用户名，`password`mysql密码，`database`数据库名。    
**PS**：数据库手动创建即可，三个不同环境创建三个database。    
**b、选择环境**  
`manage.py`中`create_app`函数默认是`default`，对应config.py中的`development`类。  

### 4、创建数据表
Python Shell模式启动项目：
```
python manage.py shell
```
即会进入python的shell，此时输入：  
```
db.create_all()
```
会在`database`中（database必须已存在），创建`app/models.py`里的所有表。    

### 5、生成一个管理员帐户
在app/models.py中，User类下有create_administrator()方法，改成你自定义的管理员帐户  
Python Shell模式启动项目：  
```
python manage.py shell
```
生成即可：
```
User.create_administrator()
```

### 6、运行
```
python manage.py runserver
```
浏览器输入`localhost:5000`，就可以看到页面。  

### 7、生成一些虚拟数据
我在app/models.py中提供了生成虚拟数据的静态方法，用于生成虚拟的用户，文章、评论和标签。  
方便测试分页导航，和一些需要数据的其他功能。
Python Shell模式启动项目：  
```
python manage.py shell
```
生成虚拟用户：
```
User.generate_fake()
```
生成虚拟文章：
```
Blog.generate_fake()
```
生成虚拟评论：
```
Comment.generate_fake()
```
生成虚拟标签：
```
Label.generate_fake()
```

