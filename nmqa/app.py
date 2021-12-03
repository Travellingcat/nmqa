from flask import Flask,session,g
import config
from exts import db,mail
from blueprints import qa_bp
from blueprints import user_bp
from flask_migrate import Migrate
from models import UserModel


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

app.register_blueprint(qa_bp)
app.register_blueprint(user_bp)


# 钩子函数
@app.before_request
def before_request():
    user_id = session.get("user_id")
    # 如果存在session
    if user_id:
        try:
            user = UserModel.query.get(user_id)
            # 给g这个flask的全局变量绑定一个user变量,它的值是上面的user模型
            g.user = user
        except:
            pass

# 请求 -> before_request -> 视图函数 -> 返回模板 -> context_processor

# 上下文处理器
@app.context_processor
def context_processor():
    # 判断g这个全局变量是否绑定了user变量
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}


if __name__ == '__main__':
    app.run()
