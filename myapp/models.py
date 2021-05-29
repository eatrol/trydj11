from django.db import models

# 如果 Models.py 的資料庫有做修改, 必須同步
# >> python3 manage.py makemigrations
# >> python3 manage.py migrate

# 定義資料庫格式(cName,cSex,cBirthday,cEmail,cPhone,cAddr) ===============


class ericpro(models.Model):
	name = models.CharField(max_length=20, null=False)
	cata = models.CharField(max_length=20, null=False) 
	subcata = models.CharField(max_length=20, null=False)
	isnew = models.IntegerField (default=1)
	isprice = models.IntegerField(default=1)
	price = models.DecimalField(max_digits=7, decimal_places=2,default=100)
	image = models.CharField(max_length=50, blank=True, default='img/product-8.png')
	stock = models.CharField(max_length=255,blank=True, default='')
	#image1 = models.ImageField() # 只想上傳照片到特定資料夾'logo',檔名不改
	image1 = models.ImageField(upload_to='pphoto',blank=True, default='eee')
	image2 = models.ImageField(upload_to='pphoto',blank=True, default='bb') 
	image3 = models.ImageField(upload_to='pphoto',blank=True, default='c')
	description = models.CharField(max_length=500, null=False, default='this is my first website')

	def __str__(self):
		return self.name



# =============================

class ericorder(models.Model):
	name = models.CharField(max_length=50, blank=True, default='')
	accept = models.BooleanField(default=False)
	status = models.CharField(max_length=100, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	shoplist = models.CharField(max_length=100, null=True)
	shopqty = models.CharField(max_length=100, null=True)
	shopprice = models.CharField(max_length=100, null=True)
	cName = models.CharField(max_length=50, blank=True, default='')
	cPhone = models.CharField(max_length=50, blank=True, default='')
	cAddress = models.CharField(max_length=100, blank=True, default='')
	cMail = models.CharField(max_length=100, blank=True, default='')
	tradeinfo = models.CharField(max_length=1000, null=True)
	tradesha256 = models.CharField(max_length=1000, null=True)

	def __str__(self):
		return self.name


class ericuser(models.Model):
	name = models.CharField(max_length=50, blank=True, default='')
	userid = models.CharField(max_length=50, blank=True, default='')
	password = models.CharField(max_length=50, blank=True, default='')	
	score = models.DecimalField(max_digits=7, decimal_places=2)
	data = models.CharField(max_length=50, blank=True, default='')
	def __str__(self):
		return self.name
