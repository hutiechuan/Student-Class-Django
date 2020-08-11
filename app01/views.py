from django.http import HttpResponse
from django.shortcuts import render,redirect
import pymysql
import json
from utils.sqlhealper import modify


def classes(requests):
    conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',password='',database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select class_id,title from class")
    class_list = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(requests,'classes.html',{'class_list':class_list})


def add_class(request):
    if request.method == 'GET':
        return render(request, 'add_class.html')
    else:
        v = request.POST.get('title')
        if (len(v)>0):
            conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
            cursor = conn.cursor()
            cursor.execute("insert into class (title) values (%s)",v)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('/classes')
        else:
            return render(request, 'add_class.html',{'msg':'班级名称不能为空'})

def del_class(request):
    nid=request.GET.get('nid')
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from class where class_id=%s", nid)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/classes')

def del_student(request):
    nid = request.GET.get('nid')
    print(nid)
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("delete from student where id=%s", nid)
    conn.commit()
    cursor.close()
    conn.close()
    return redirect('/student')

def edit_class(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("select class_id,title from class where class_id = %s", nid)
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return render(request,'edit_class.html',{'result':result})
    else:
        nid = request.POST.get('class_id')
        print(nid)
        title= request.POST.get('title')
        print(title)
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("update class set title=%s where class_id=%s", [title,nid])
        result = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/classes')

def student(requests):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("SELECT id,name,title from student LEFT JOIN class on student.class_id = class.class_id;")
    student_list = cursor.fetchall()
    class_list = sqlhealper.get_list('select class_id,title from class',[])
    return render(requests, 'student.html', {'student_list': student_list,'class_list':class_list})


def add_student(requests):
    if requests.method == 'GET':
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("SELECT * from class")
        student_list = cursor.fetchall()
        return render(requests, 'add_student.html', {'student_list': student_list})
    else:
        name = requests.POST.get('name')
        cls = requests.POST.get('student_id')
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', database='db3')
        cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute("insert into student (name,class_id) values (%s,%s)",[name,cls])
        print(name)
        print(cls)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect('/student')

from utils import sqlhealper

def edit_student(request):
    if request.method == 'GET':
        nid = request.GET.get('nid')
        class_list = sqlhealper.get_list("select class_id,title from class",[])
        current = sqlhealper.get_one('select id,name,class_id from student where id = %s',nid)
        return render(request,'edit_student.html',{'class_list':class_list,'current_info':current})
    else:
        nid = request.GET.get('nid')
        name= request.POST.get('name')
        cls = request.POST.get('class_id')
        print(nid,name,cls)
        modify('update student set name =%s, class_id=%s where id=%s',[name,cls,nid])
        return redirect('/student')


###########对话框###############
def modal_add_class(request):
    title = request.POST.get('title')
    print(title)
    if title != None:
        sqlhealper.modify('insert into class (title) values (%s)', title)
        return HttpResponse('ok')
    else:
        return HttpResponse('不ok')
#     sqlhealper.modify('insert into class (title) values (%s)',title)
#     return redirect('/classes/')

def modal_edit_class(request):
    nid = request.POST.get('nid')
    content = request.POST.get('content')
    sqlhealper.modify("update class set title=%s where class_id=%s",[content,nid])
    return redirect('/classes/')


def layout(request):
    return render(request,'layout.html')