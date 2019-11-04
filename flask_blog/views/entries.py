from flask import request, redirect, url_for, render_template,flash, session
from flask_blog import app
from flask_blog.models.entries import Entry
from flask_login import login_required
from datetime import datetime

@app.route('/')
@login_required
def show_entries():
    entries = Entry.scan()#PynamoDBのメソッド。すべての記事を取得
    entries = sorted(entries, key=lambda x: x.id, reverse=True)#timestamp順に記事をソート。
    return render_template('entries/index.html', entries = entries)

@app.route('/entries', methods=['POST'])#記事を追加。POSTを指定しないとGETメソッドのみになる。
@login_required
def add_entry():
    #新規モデル（レコード）をデータベースに登録
    entry = Entry(
        id=int(datetime.now().timestamp()),
        title= request.form['title'],#属性=カラム
        text = request.form['text']
    )
    entry.save()
    flash('新しく記事が作成されました')
    return redirect(url_for('show_entries'))#登録後はリダイレクト

@app.route('/entries/new', methods=['GET'])#記事の新規追加フォームを表示
@login_required
def new_entry():
    return render_template('entries/new.html')#普通にHTMLを返す。

@app.route('/entries/<int:id>', methods=['GET'])
@login_required
def show_entry(id):
    entry = Entry.get(id)
    return render_template('entries/show.html', entry=entry)


@app.route('/entries/<int:id>/edit', methods=['GET'])
@login_required
def edit_entry(id):
    entry = Entry.get(id)
    return render_template('entries/edit.html', entry=entry)

@app.route('/entries/<int:id>/update', methods=['POST'])#記事の更新
@login_required
def update_entry(id):
    entry = Entry.get(id)#記事を取得
    entry.title = request.form['title']#属性を指定して直接代入して値を更新
    entry.text = request.form['text']
    entry.save()
    flash('記事が更新されました')
    return redirect(url_for('show_entries'))

@app.route('/entries/<int:id>/delete', methods=['POST'])#記事の削除
@login_required
def delete_entry(id):
    entry = Entry.get(id)
    entry.delete()#データを削除
    flash('記事が更新されました')
    return redirect(url_for('show_entries'))
