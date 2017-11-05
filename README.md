# myblog
本项目是由Python实现的个人博客网站。 [网站地址](www.jiyuankai.top)  
后端使用**Python3**编写，基于**Flask**框架，并以**Jinja2**作为模板引擎。使用**MySQL**数据库。前端部分使用的是**bootstrap** CSS框架。  
项目部署在阿里云，服务器操作系统为**Ubuntu 16.04**，使用**Gunicorn**处理动态请求，搭配**gevent**库实现异步响应。前端反向代理服务器使用**Nginx**。监测使用**Supervisor**来守护进程。    
开发相关日志可以在[CSDN博客](http://blog.csdn.net/jyk920902)中查看。   
# 项目结构
|-myblog  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-config.py 配置文件  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-manage.py 用于启动程序  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-app/保存所有的Flask程序  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-\_\_init\_\_.py初始化Flask文件  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-models.py数据库模型  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-templates/模板文件夹  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-static/静态文件夹  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-main/  mian蓝图文件夹  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-views.py 视图函数  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-forms.py 表单  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-errors.py HTTP错误  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-manage/ manage蓝图文件夹  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|-auth/  auth蓝图文件夹  
# 入口  
**后端API**  
/comment/disable/\<int:id\> 屏蔽评论  
/comment/enable/\<int:id\>  恢复评论  
/user/disable/\<int:id\>    封禁用户  
/user/enable/\<int:id\>     解禁用户  
/delete-blog/\<int:id\>     删除文章  
/manage/create-blog 写文章页面  
/blog/\<int:id\>  写评论  

**用户浏览页面：**  
/index 主页  
/blog/\<id\> 文章详情页  
/blog/\<id\>#comments 文章评论列表  

**后台管理页面：**  
/manage/change-password 密码修改页面  
/manage/blogs 文章管理页面  
/manage/users 用户管理页面  
/manage/comments 评论管理页面  
/manage/edit-blog/\<id\>  编辑文章页面  

**验证页面：**  
/auth/login 登录  
/auth/register 注册  
/auth/logout  登出

# 开发日志

**2017-9-20**  
原网站基于python3.5的**asyncio**和 **aiohttp**库开发，实现异步响应。前端使用**uikit** CSS框架。
自行构建了Web和ORM框架，数据库使用**MySQL**。

**2017-10-20**  
决定使用**Flask** + **bootstrap**重构网站前后端。ORM框架选用**SQLAlchemy**。  

**2017-10-28**  
历时一周，完成了后端和前端的重构。

**2017-11- 1**  
网站在阿里云部署上线，进行审核备案，网站域名[www.jiyuankai.top](http://www.jiyuankai.top)。  

**2017-11- 4**    
新增**文章分类**功能：  
1、创建/修改日志时可以添加/删除文章分类标签；  
2、主页和文章详情页标题下方显示分类标签；  
3、主页右侧添加分类栏，可选择要显示的文章类型。  

**2017-11- 6**   
新增**收藏**功能：  
1、增加收藏夹页面，用于浏览和管理已收藏文章；  
2、右侧下拉导航增加**收藏管理**入口，用于进入收藏页面；  
3、文章详情页显示收藏/取消收藏按钮；  
