#### 实现环境：
- 操作系统：Windows 11 
- Idea：PyCharm 2021.3.1 (Community Edition)
- 后端：django
- 前端：基于django和bootstrap实现
- 浏览器：edge
#### 整体信息
- 基于django框架进行搭建
- 使用bootstrap，html和css实现前端
- 数据库模型：
![img](.\1.png)
####  基本使用方式
- 进入canteen_deliver目录下运行  ` python manage.py runserver `
-  随后会发现出现错误，这是因为要需要先导入数据库，
使用mysql作为数据库，建立canteen数据库，并运行由powerdesign生成的sql脚本，
或者使用django的命令 `python manage.py makemigrations` 和 ` python manage.py migrate  `
即可反向将django中的模型导入数据库中
- 导入成功后再次运行runsever即可成功访问网页

#### 基本结构
- 路由配置
	路由配置在django 的urls中。
-  视图结构
视图的结构在views文件中，负责处理业务逻辑，这与平常的MVC有所不同，这种是MTV模式
- 模型配置
模型配置在models文件中，本工程全部配置在dish的models文件中
