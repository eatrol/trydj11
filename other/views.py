from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def setS(request):
    request.session['myname'] = "張三"
    return HttpResponse('已經設定session變數')

def getS(request):
    n1 = request.session['myname']
    return HttpResponse('取得session變數 = ' + n1)

def isMember(request):
    if not "login" in request.session:
        request.session['login'] = True
        return HttpResponse('會員現在登入')
    else:
        return HttpResponse('會員已經在線上')

def setStime(request):
    if 'myname' in request.session:
        request.session.set_expiry(60*60) #60分鐘
        return HttpResponse('已經設定session變數：myname有效時間為：60分鐘' )
    else:
        return HttpResponse('沒有這個session變數：myname ')

def delS(request):
    #刪除myname
    #del request.session['myname']
    #刪除全部的session
    request.session.clear()
    return HttpResponse('已經清除全部的session變數')

def login(request):
    if request.method == "POST":
        if not 'username' in request.session:
            if request.POST['myname'] == 'john' and request.POST['mypw'] == 'john':
                request.session['username'] = request.POST['myname']
                request.session['password'] = request.POST['mypw']
                login = True
                message = '歡迎光臨，' + request.session['username'] + '你登入了'
            else:
                message = '帳號密碼錯誤!'
        else:
            login = True
            message = request.session['username'] + '，你已經在線上了'
    return render(request,'login.html',locals())

def getSS(request):
    n1 = request.session['username']
    return HttpResponse('取得session變數 = ' + n1)


def logout(request):
    if 'username' in request.session:
        login = False
        message = '再見，' + request.session['username'] + '，你登出了'
        del request.session['username']
        del request.session['password']
    return render(request,'login.html',locals())

def shownum(request):
    if 'num' in request.COOKIES:
        num = int(request.COOKIES['num'])
        num += 1
    else:
        num = 1
    rsp = HttpResponse('網頁瀏覽人數 = '+ str(num))
    rsp.set_cookie('num',num)
    return rsp
