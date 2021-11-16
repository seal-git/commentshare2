from app import app_, db_, login_manager
from flask import request, jsonify
from app.db_define import User,PDF,Comment,Follow
import os
import json
import datetime
import pytz
from sqlalchemy import and_
from flask_login import login_user, current_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app_.route('/api_test', methods=['POST'])
def api_test():
    json_data = request.json
    return "success"


@app_.route('/add_comments', methods=['POST','GET'])
def add_comments():
    print(os.getcwd())
    if request.method == 'POST':
        result = request.get_json()
        print(result)
        if current_user.is_active:
            user_id = current_user.id
            username = current_user.username
        else:
            user_id = "-1"
            username = "guest"

        comment = Comment(
            value=result['value'],
            user_id=user_id,
            user_name=username,
            pdf_id=result['pdf_id'],
            span_page=result['span-page'],
            span_top=result['span-top'],
            span_left=result['span-left'],
            created=datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
            )
        db_.session.add(comment)
        db_.session.commit()

    return "success"


@app_.route('/get_comments', methods=['POST','GET'])
def get_comments():
    print(os.getcwd())
    param = request.get_json()
    pdf_id=int(param["pdf_id"])
    comments = db_.session.query(Comment).filter_by(pdf_id=pdf_id).all()
    length=len(comments)
    comments_list=list()
    for i in range(length):
        dict={}
        dict['id']=comments[i].id
        dict['name']=comments[i].user_name
        dict['value']=comments[i].value
        dict['span-page']=str(comments[i].span_page)
        dict['span-top']=comments[i].span_top
        dict['span-left']=comments[i].span_left
        dict['time']=str(comments[i].created)
        comments_list.append(dict)
    #print(comments_list)
    comments_list=json.dumps(comments_list,ensure_ascii=False)
    if request.method=='POST':
        return comments_list
    else:
        return 'get'



@app_.route('/get_user', methods=['POST'])
def get_user():
    json_data = request.json
    user_id = int(json_data['user_id'])
    if user_id != -1:
        user = db_.session.query(User).filter_by(id=user_id).one()
    else:
        return 'guest'
    get_user = dict()
    get_user['profile'] = user.profile
    get_user['email'] = user.email
    get_user['user_name'] = user.username
    get_user = json.dumps(get_user,ensure_ascii=False)
    return get_user


@app_.route('/word_search', methods=['POST','GET'])
def word_search():
    if request.method=='POST':
        json_data = request.json
        keyword = json_data['query']
        keyword='%'+keyword+'%'
        pdfs = db_.session.query(PDF).filter(PDF.filename.ilike(keyword)).all()
        len_pdfs=len(pdfs)
        pdf_list=list()
        if len_pdfs>0:
            for i in range(len_pdfs):
                dict={}
                dict['id']=pdfs[i].id
                dict['filename']=pdfs[i].filename
                dict['url']=pdfs[i].url
                pdf_list.append(dict)
            pdf_list = json.dumps(pdf_list,ensure_ascii=False)
            return pdf_list
        else:
            return 'no_finding'


@app_.route('/add_follow', methods=['POST'])
def add_follow():
    json_data = request.json
    follow_from =json_data['follow_from']
    follow_to =json_data['follow_to']
    follow =Follow(
        follow_from = follow_from,
        follow_to = follow_to
    )
    db_.session.add(follow)
    db_.session.commit()
    return "success"


@app_.route('/delete_follow', methods=['POST'])
def delete_follow():
    json_data = request.json
    follow_from =json_data['follow_from']
    follow_to =json_data['follow_to']
    follow = db_.session.query(Follow).filter_by(follow_to=follow_to).filter_by(follow_from=follow_from).first()
    db_.session.delete(follow)
    db_.session.commit()
    return "success"



@app_.route('/get_follow', methods=['POST'])
def get_follow():
    json_data = request.json
    follow_from =json_data['id']
    follows = db_.session.query(Follow.follow_to ,User.username,User.profile
                               ).filter_by(follow_from=follow_from).join(User,User.id == Follow.follow_to).all()
                            
    follow_list=list()
    if len(follows)>0:
        for i in range(len(follows)):
            dict={}
            dict['id']=follows[i].follow_to
            dict['username']=follows[i].username
            dict['profile']=follows[i].profile
            follow_list.append(dict)
        follow_list = json.dumps(follow_list,ensure_ascii=False)
        return follow_list

    return "no_follows"


@app_.route('/follow_check', methods=['POST'])
def follow_check():
    json_data = request.json
    follow_from =json_data['follow_from']
    follow_to =json_data['follow_to']
    follows = follow = db_.session.query(Follow).filter_by(follow_to=follow_to).filter_by(follow_from=follow_from).first()                          
    if len(follows)>0:
           return True

    return False


@app_.route('/and_word_search', methods=['POST','GET'])
def and_word_search():
    if request.method=='POST':
        json_data = request.json
        keyword = json_data['query']
        keyword = keyword.split(' ')
        filters = []
        for k in keyword:
            k = '%'+k+'%'
            filters.append(PDF.filename.ilike(k))
        pdfs = db_.session.query(PDF).filter(and_(*filters)).all()
        len_pdfs=len(pdfs)
        pdf_list=list()
        if len_pdfs>0:
            for i in range(len_pdfs):
                dict={}
                dict['id']=pdfs[i].id
                dict['filename']=pdfs[i].filename
                dict['url']=pdfs[i].url
                pdf_list.append(dict)
            pdf_list = json.dumps(pdf_list,ensure_ascii=False)
            return pdf_list
        else:
            return 'no_finding'



