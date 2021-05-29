from django.shortcuts import render


# Create your views here.
def cuthello(request):
    return render(request, "hello.html", locals())


# Create your views here.
def cutphoto(request):
    return render(request, "cutphoto.html", locals())

def cutphotos(request,pk):
    if pk == "hero" :
        width = "1900px"
        height = "650px"
    elif pk == "pro":
        width = "606px"
        height = "666px"  
    else :
        width = "100px"
        height = "100px"        

    return render(request, "cutphoto.html", locals())

# Create your views here.
