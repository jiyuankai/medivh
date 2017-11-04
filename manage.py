import os
from app import create_app, db
from app.models import User, Blog, Comment, Label
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('FLASK_CONFIG') or 'default') #os.getenv('FLASK_CONFIG') or 'default'
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
    return dict(app=app, db=db, User=User, Blog=Blog, Comment=Comment, Label=Label)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)

# 自定义命令，以函数名
@manager.command
def test():
    # 启动单元测试
    import unittest
    # 传入path寻找测试文件文件夹
    tests = unittest.TestLoader().discover('tests')
    # 读取测试文件并运行测试
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def deploy():
    from flask_migrate import upgrade
    
    upgrade()
    Blog.create_about_blog()


if __name__ == '__main__':
    manager.run()
