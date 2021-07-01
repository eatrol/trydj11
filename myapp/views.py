#from typing_extensions import Required
from django.shortcuts import render,redirect
from myapp.models import ericpro,ericorder,ericuser
from django.http import HttpResponse    # 把HttpResponse叫進來用
import time
import hashlib
from cryptography import *
from Crypto.Cipher import AES


# 寄送email所需要的
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string # 若寄送HTML郵件需此行


# Create your views here.
def sayhello(request):
    return render(request, "hello.html", locals())

def mario(request):
    return render(request, "game3.html", locals())

def fishing(request):
    return render(request, "fish2.html", locals())

def index(request):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    students = ericpro.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    return render(request, "index.html", locals())

def knitgallery(request):
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    # 列出商品 ---
    
    students = ericpro.objects.all().order_by('id') 
    students_sum = students.count()
    return render(request,"knitgallery.html",locals())

def blog(request):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    return render(request, "blog.html", locals())

def aboutus(request):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    return render(request, "aboutus.html", locals())

#========= ADMIN 商品管理 ==========================================================
def adminlistpro(request):
    students = ericpro.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    return render(request,"admin_listpro.html",locals())

def adminformpro(request,pk):
    product = ericpro.objects.get(id=pk)
    icata = {'記號圈':'','收納本':'','毛線':''}
    icata[product.cata] = "selected"
    isubcata = {'花草系列':'','可愛動物':'','日式和風':'','中國風':'','數字圈':'','銀白世界':'','萬聖節':'','卡通':'','其他':''}
    isubcata[product.subcata] = "selected"
    return render(request,"admin_formpro.html",locals())

def adminupdatepro(request):
    pk = request.POST['fid']
    unit = ericpro.objects.get(id=pk)
    unit.name = request.POST['fname']
    unit.price = request.POST['fprice']
    unit.stock = request.POST['fstock']
    unit.cata = request.POST['fcata']
    unit.isnew = request.POST['fisnew']
    unit.isprice = request.POST['fisprice']
    unit.subcata = request.POST['fsubcata']
    unit.image = request.POST['fimage']
    unit.save()  #寫入資料庫
    students = ericpro.objects.all().order_by('isnew')  #讀取資料表, 依 id 遞增排序
    return render(request,"admin_listpro.html",locals())


# 自訂上傳圖面
def adminuploadphoto(request,pk):
    product = ericpro.objects.get(id=pk)
    ff1 = request.FILES['logo']
    ff2 = request.POST['fimage']
    if ff1:
        print(ff2)
        if ff2 == "image1":
            product.image1 = ff1
        elif ff2 == "image2":
            product.image2 = ff1
        elif ff2 == "image3":
            product.image3 = ff1     
        product.save()

    icata = {'記號圈':'','收納本':'','毛線':''}
    icata[product.cata] = "selected"
    isubcata = {'花草系列':'','可愛動物':'','日式和風':'','中國風':'','數字圈':'','銀白世界':'','萬聖節':'','卡通':'','其他':''}
    isubcata[product.subcata] = "selected"
    return render(request,"admin_formpro.html",locals())


#====================================================================================

#========= ADMIN 訂單管理 ==========================================================
def adminlistorder(request):
    students = ericorder.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    return render(request,"admin_listorder.html",locals())

def adminlistordersearch1(request):
    pk = request.POST['f1status']
    students = ericorder.objects.filter(status=pk) 
    return render(request,"admin_listorder.html",locals())   

def adminlistordersearch2(request):
    pk = request.POST['f1status']
    fname = request.POST['fname']
    print(fname)
    if pk == "cName":
        students = ericorder.objects.filter(cName__contains=fname) 
    if pk == "cPhone":
        students = ericorder.objects.filter(cPhone__contains=fname) 
    if pk == "cMail":
        students = ericorder.objects.filter(cMail__contains=fname) 
    if pk == "cAddress":
        students = ericorder.objects.filter(cAddress__contains=fname)    

    return render(request,"admin_listorder.html",locals()) 

def adminformorder(request,pk):
    product = ericorder.objects.get(id=pk)
    sId = product.shoplist
    sQty =product.shopqty
    sPrice = product.shopprice
    istatus = {'訂單待處理':'','訂單處理中':'','等待付款':'','已付款待出貨':'','已出貨':'','已到貨':''}
    istatus[product.status] = "selected"
    iaccept = {'True':'','False':''}
    iaccept[str(product.accept)] = "selected"   
    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [order,clist_sum] = showorder(sId,sQty,sPrice)

    return render(request,"admin_formorder.html",locals())


def adminupdateorder(request):
    pk = request.POST['fid']
    unit = ericorder.objects.get(id=pk)
    unit.name = request.POST['fname']
    unit.cName = request.POST['fcName']
    unit.cPhone = request.POST['fcPhone']
    unit.cMail = request.POST['fcMail']
    unit.cAddress = request.POST['fcAddress']
    unit.status = request.POST['fstatus']
    unit.shopprice = request.POST['fshopprice']
    unit.shoplist = request.POST['fshoplist']
    unit.shopqty = request.POST['fshopqty']
    unit.price = request.POST['fprice']
    #print(request.POST['faccept'],bool(request.POST['faccept']),bool(''),bool('1'))
    unit.accept = bool(request.POST['faccept'])
    unit.save()  #寫入資料庫
    students = ericorder.objects.all().order_by('accept')  #讀取資料表, 依 id 遞增排序
    return render(request,"admin_listorder.html",locals())

def admindelorder(request,pk):  #刪除資料
    unit = ericorder.objects.get(id=pk)
    unit.delete()
    students = ericorder.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
    return render(request,"admin_listorder.html",locals())

#===================================================================





def listall(request):  
	students = ericpro.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
	return render(request, "listall.html", locals())

def knitshop(request):  
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    # 列出商品 ---
    students = ericpro.objects.all().order_by('id') 
    students_sum = students.count()
    return render(request,"knitshop.html",locals())

def subcata(request,pk):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    students = ericpro.objects.filter(subcata=pk)    
    students_sum = students.count()
    if not students_sum:
        students_sum = 0
    return render(request, "knitshop.html", locals())

def cata(request,pk):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    students = ericpro.objects.filter(cata=pk)     
    students_sum = students.count()
    return render(request, "knitshop.html", locals())

def checkout(request):  
    if not "shopitem" in request.session:
        request.session['shopitem'] = 'xxx'
        request.session['shopqty'] = 'xxx'

    # 讀取session 中的數值
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])

    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)

    # 更新購物車數量的數量 :
    cart_sum=getcartsum(request.session['shopitem'])

    return render(request, "checkout.html",locals())



def addorder(request):

    # 將訂單資訊轉成 AES , SHA256格式
    def newebpay(name,price):
        tradeword = 'MerchantID=MS1474192347&RespondType=JSON&TimeStamp=1618970641&Version=1.6&MerchantOrderNo='+ str(name) +'&Amt=' + str(price) +'&ItemDesc=記號圈&Email=eatrol%40gmail.com&ClientBackURL=http://www.knittingtime.club&ReturnURL=http://www.knittingtime.club/aboutus'
        key = 'JC8kARMt4weqXERE60ddbmVAaPSgd4mI'
        iv =  'PHM9j1YF2PmKWEwC'

        data = tradeword.encode("utf8")
        length = 32 - (len(data) % 32)
        data += bytes([length])*length    

        cryptor = AES.new(key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
        ciphertext = cryptor.encrypt(data)        # 這是 Bytes的格式
        tradeinfo = ciphertext.hex()         #  轉換成16進位格式  

        sha = 'HashKey=' + key + '&' + tradeinfo + '&HashIV=' + iv    
        sha256 = hashlib.sha256(sha.encode('utf-8')).hexdigest()
        tradesha256 = str.upper(sha256)  

        return tradeinfo,tradesha256

    def trymail2():
        ordertime = name[1:4] + '-' + name[5:6] + '-' + name[7:8] + '  ' + name[9:10] + ':' + name[11:12] 
        clist_pay = clist_sum + 40
        email_template = render_to_string(
            'mail_NewOrder.html',
            { 'name': name,'cName': cName,'cPhone': cPhone,'cMail': cMail,'cAddress': cAddress,'order': order,'clist_sum': clist_sum, 'clist_pay': clist_pay, 'ordertime': ordertime,}
        )

        email = EmailMessage(
                '[編織時光] 謝謝你的訂單 #' + name ,       # 電子郵件標題
                email_template,            # 電子郵件內容
                settings.EMAIL_HOST_USER,  # 寄件者
                ['luerichl@gmail.com']     # 收件者
            )

        email.content_subtype = 'html'  # 此行一定要有, 才會用HTML開啟mail
        email.fail_silently = False
        email.send()





    name = time.strftime("%Y%m%d%H%M%S")
    accept =  False
    status =  '訂單待處理'
    shoplist = str(request.session['shopitem'])
    shopqty =  str(request.session['shopqty'])
    shopprice = getshopprice(shoplist)
    cName =  request.POST['check_cName1'] + ' ' + request.POST['check_cName2']
    cPhone = request.POST['check_cPhone']
    cAddress = request.POST['check_cAddress1']
    cMail = request.POST['check_cMail']
    price = request.POST['check_price']
    price = int(float(price))
      
    [tradeinfo,tradesha256] = newebpay(name,price)

    unit = ericorder.objects.create(name=name, accept=accept, status=status, shoplist=shoplist,shopqty=shopqty, cName=cName,cPhone=cPhone,cAddress=cAddress,cMail=cMail,price=price,shopprice=shopprice,tradeinfo=tradeinfo,tradesha256=tradesha256) 
    unit.save()  #寫入資料庫
  
    # 讀取session 中的數值
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])

    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)
    del request.session['shopitem']
    del request.session['shopqty']

    trymail2()

    return render(request, "orderinfo.html", locals())

 


def getorder(request,pk):
    try:
        unit = ericorder.objects.get(name=pk) 
 

        sId = str(unit.shoplist)
        sQty =str(unit.shopqty)
        # 轉換成矩陣格式 clist_sum:總價,order:total項目
        [clist,clist_sum,order] = showcart(sId,sQty)
        name = pk
        tradeinfo = unit.tradeinfo
        tradesha256 = unit.tradesha256
        return render(request, "orderinfo.html", locals())
    except:
        return HttpResponse("Wrong order number")


#會員登錄系統===================

def login(request):  
    userid = request.POST['inputId']       # 抓網頁輸入了帳號欄位
    userpass = request.POST['inputPass']   # 抓網頁輸入的密碼欄位
    userid = userid.upper() # 轉換成大寫 (帳號一律用大寫)

    try:
        unit = ericuser.objects.get(userid = userid, password=userpass)
        login = True
        request.session['username'] = unit.userid
        return redirect("/userpage/")
    

    except ericuser.DoesNotExist:
        fffid = "帳號密碼錯誤"
        return render(request, "login.html", locals())


def logout(request):
    if 'username' in request.session:
        login = False
        del request.session['username']
        
    return redirect("/userpage/")

def userpage(request):  
    if 'username' in request.session:
        print("找到使用者")
        
        userid = str(request.session['username'])
        print("找到資料庫")
        unit = ericuser.objects.get(userid = userid)
        print("沒問題")
        return render(request, "userpage.html", locals())
    else:
        return render(request, "login.html", locals())


def newuser(request):
    userid = request.POST["fuserid"]
    password = request.POST["fpassword"]
    usermail = request.POST["fusermail"]
    name = request.POST["fname"]
    address = request.POST["faddress"]
    phone = request.POST["fphone"]
    facebook = request.POST["ffacebook"]

    userid = str(userid.upper())


    print(userid)

    # 確認帳號/密碼/信箱不是空白
    if userid == "" :
        return HttpResponse("user should not be empty!")
    if password == "" :
        return HttpResponse("password should not be empty!")
    if usermail == "" :
        return HttpResponse("e-mail should not be empty!")

    try:
        unit = ericuser.objects.get(userid = userid)
        return HttpResponse("已有此會員帳號")
    except:
        print("hi")
        
        unit = ericuser.objects.create(userid = userid,password = password, usermail= usermail ,score=0, name=name ,phone = phone, address = address, facebook = facebook ) 
        unit.save()  #寫入資料庫
        request.session['username'] = unit.userid
        return redirect("/userpage/")
        
        #return HttpResponse("會員已建立")


#=======================================


def main(request):  
	students = ericpro.objects.all().order_by('id')  #讀取資料表, 依 id 遞增排序
	return render(request, "main.html",locals())


def product(request, pk):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    product = ericpro.objects.get(id=pk)
    students = ericpro.objects.all().order_by('id') 
    students = students[0:4]
    return render(request,"detail.html",locals())
#    return render(request,"awesome.html",locals())

def addcart(request):
    s1 = request.POST['sitem']   
    s2 = request.POST['squantity']

    if not "shopitem" in request.session:
        n1 = 'xxx/'+ str(s1)
        n2 = 'xxx/'+ str(s2)
    else:
        n1 = request.session['shopitem']
        n2 = request.session['shopqty']

        nn1 = str(n1).split('/')
        nn2 = str(n2).split('/')
        if s1 in nn1:
          pk = nn1.index(s1)
          nn2[pk] = str(int(nn2[pk]) + int(s2))
          n1 = "/".join(nn1)
          n2 = "/".join(nn2)
        else:
            n1 = n1 + '/' + str(s1)
            n2 = n2 + '/' + str(s2)
        
    # =====
    request.session['shopitem'] = n1
    request.session['shopqty'] = n2

    # 顯示購物車
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])
    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)

    # 更新購物車數量的數量 :
    cart_sum=getcartsum(request.session['shopitem'])

    return render(request,"knitcart.html",locals())
    

def addtocart(request,pk):

    s1 = pk
    s2 = 1

    if not "shopitem" in request.session:
        n1 = 'xxx/'+ str(s1)
        n2 = 'xxx/'+ str(s2)
    else:
        n1 = request.session['shopitem']
        n2 = request.session['shopqty']

        nn1 = str(n1).split('/')
        nn2 = str(n2).split('/')
        if s1 in nn1:
          pk = nn1.index(s1)
          nn2[pk] = str(int(nn2[pk]) + int(s2))
          n1 = "/".join(nn1)
          n2 = "/".join(nn2)
        else:
            n1 = n1 + '/' + str(s1)
            n2 = n2 + '/' + str(s2)
        
    # =====
    request.session['shopitem'] = n1
    request.session['shopqty'] = n2

    # 顯示購物車
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])
    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)

    # 更新購物車數量的數量 :
    cart_sum=getcartsum(request.session['shopitem'])

    return render(request,"knitcart.html",locals())
    #return HttpResponse('購買清單: ' + n1 + '  購買數量' + n2)


def cart(request):
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    if not "shopitem" in request.session:
        request.session['shopitem'] = 'xxx'
        request.session['shopqty'] = 'xxx'
    # 讀取session 中的數值
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])

    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)

    return render(request,"knitcart.html",locals())



def removecart(request):
    act = request.POST['revbtn'].split('-')
    print(act)
    pk = int(act[1])

    sId = str(request.session['shopitem'])
    sId = sId.split('/')
    sQty =str(request.session['shopqty'])
    sQty = sQty.split('/')

    if act[0] == 'rem' :
        del sId[pk] 
        del sQty[pk]

    elif act[0] == 'add':
        sQty[pk] = str(int(sQty[pk]) + 1)

    elif act[0] == 'cut' and int(sQty[pk]) > 1:
        sQty[pk] = str(int(sQty[pk]) - 1)
    
    
    s1 = "/".join(sId)
    s2 = "/".join(sQty)

    request.session['shopitem'] = s1
    request.session['shopqty'] = s2
        
    sId = str(request.session['shopitem'])
    sQty =str(request.session['shopqty'])

    # 轉換成矩陣格式 clist_sum:總價,order:total項目
    [clist,clist_sum,order] = showcart(sId,sQty)

    # 更新購物車數量的數量 :
    cart_sum=getcartsum(request.session['shopitem'])
 
    return render(request,"knitcart.html",locals())

#=======手機版網頁========================
def mknitshop(request):  
    # 更新購物車數量的數量 :
    if not "shopitem" in request.session:
        cart_sum="0"
    else:
        cart_sum=getcartsum(request.session['shopitem'])

    # 列出商品 ---
    students = ericpro.objects.all().order_by('id') 
    students_sum = students.count()
    return render(request,"m_knitshop.html",locals())

#=====================
#======================


# 把 session 裏頭的訂單內容(sID) 跟數量(sQty) 轉換成矩陣式
def showcart(sId,sQty):
    # ----------
    sId = sId.split('/')
    sQty = sQty.split('/')
    
    del sId[0]  # 第0項為暫存 
    del sQty[0]

    clist=[]
    k = 1
    for i,j in zip(sId,sQty):
        product = ericpro.objects.get(id=i)
        act1 = 'rem-' + str(k)
        act2 = 'cut-' + str(k)
        act3 = 'add-' + str(k)
        bbb = [product.name, product.price, int(j),product.cata, product.price*int(j), product.id,product.image, act1,act2,act3]
        clist.append(bbb)
        k = k + 1

    clist_sum = 0
    order =[]
    for i in clist:
        bb1 = i[0] + ' * ' +str(i[2])
        bbb = [bb1 , str(i[4]), i[6]]
        order.append(bbb)
        clist_sum = i[4] + clist_sum

    return clist,clist_sum,order


def getshopprice(sId):
    sId = sId.split('/')
    del sId[0]

    shopprice ='xxx'
    for i in sId:
        product = ericpro.objects.get(id=i)
        shopprice = shopprice + '/' + str(int(product.price))
    
    return shopprice


def showorder(sId,sQty,sPrice):
    sId = sId.split('/')
    sQty = sQty.split('/')
    sPrice = sPrice.split('/')

    del sId[0]  # 第0項為暫存 
    del sQty[0]
    del sPrice[0]

    order=[]
    clist_sum=0
    for i,j,k in zip(sId,sQty,sPrice):
        product = ericpro.objects.get(id=i)
        bb1 = product.name + '*' + str(j)
        bb2 = int(k) * int(j)
        bb3 = product.image
        clist_sum = clist_sum + bb2
        bbb = [bb1,bb2,bb3]
        order.append(bbb)
        
    return order,clist_sum
           

def getcartsum(sId):
    nn1 = str(sId).split('/')
    cart_sum= len(nn1)-1   
    return cart_sum






