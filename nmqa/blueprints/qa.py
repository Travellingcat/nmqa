from flask import Blueprint,render_template,request,g,redirect,flash,url_for
from decorators import log_required
from .forms import QuestionForm,AnswerForm
from models import QuestionModel,AnswerModel
from exts import db
from sqlalchemy import or_


bp = Blueprint("qa", __name__, url_prefix="/")


@bp.route("/")
def index():
    questions = QuestionModel.query.order_by(db.text("-create_time")).all()
    return render_template("index.html", questions=questions)


# 发布问答
@bp.route("/question/public", methods=['GET', 'POST'])
@log_required
def public_question():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            flash("发布失败！")
            return redirect(url_for("qa.public_question"))


@bp.route("/question/<int:question_id>")
def question_detail(question_id):
    question = QuestionModel.query.filter_by(id=question_id).first()
    return render_template("detail.html", question=question)

@bp.route("/answer/<int:question_id>", methods=['POST'])
@log_required
def answer(question_id):
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        answer_model = AnswerModel(content=content, author=g.user, question_id=question_id)
        db.session.add(answer_model)
        db.session.commit()
        return redirect(url_for("qa.question_detail", question_id=question_id))
    else:
        flash("评论提交失败！")
        return redirect(url_for("qa.question_detail",question_id=question_id))


@bp.route("/search")
def search():
    q = request.args.get("q")
    # filter_by:直接使用字段名
    # filter:使用模型.字段名
    questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(q), QuestionModel.content.contains(q))).order_by(db.text("-create_time"))
    return render_template("index.html", questions=questions)