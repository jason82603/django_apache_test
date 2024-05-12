from django.shortcuts import render, redirect
from django.http import JsonResponse
# from .models import Data
# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from .forms import CustomUserCreationForm
from . import models

@csrf_exempt
def operation(request):
    if request.method == 'GET':
        # 返回首頁，顯示 operation.html，但不顯示任何表單
        return render(request, "operation.html")

    elif request.method == 'POST':
        action = request.POST.get('action')

        # 根據不同的 action 進行相應的處理
        if action == 'query':
            # 查詢資料
            products = models.ProductModel.objects.all()  # 取得所有的商品資料
            return render(request, "operation.html", {'action': action, 'products': products})
        #右側列表的資料新增
        elif action == 'add':
            # 有登入
            if request.user.is_authenticated:
                return render(request, "operation.html", {'action': action})
            else:
                return redirect('login')
        #左側介面的資料新增展示
        elif action == 'add_display':
            if request.user.is_authenticated:
                action = action
                user = request.user
                pname = request.POST.get('pname', '')
                pprice = request.POST.get('pprice', '')
                pdescription = request.POST.get('pdescription', '')
                unitproduct = models.ProductModel.objects.create(pname=pname, pprice=pprice, pdescription=pdescription, user=user)  # 建立訂單
                productid = unitproduct.id

                return render(request, "operation.html", locals())


        elif action == 'update':
            # 有登入
            if request.user.is_authenticated:
            # 修改資料
            # your update data logic here
                return render(request, "operation.html", {'action': action})
            else:
                return redirect('login')

        elif action == 'update_display':
            # 有登入
            if request.user.is_authenticated:
                action = action
                user = request.user
                pname = request.POST.get('pname', '')
                pprice = request.POST.get('pprice', '')
                pdescription = request.POST.get('pdescription', '')
                productid = request.POST.get('productid', '')

                # 取得要更新的商品
                product = models.ProductModel.objects.get(pk=productid)
                # 更新商品資料
                product.pname = pname
                product.pprice = pprice
                product.pdescription = pdescription
                # 儲存更新後的資料
                product.save()
            # your update data logic here
                return render(request, "operation.html", locals())

        elif action == 'delete':
            # 有登入
            if request.user.is_authenticated:
            # 刪除資料
            # your delete data logic here
                return render(request, "operation.html", {'action': action})
            else:
                return redirect('login')

        elif action == 'delete_display':
            if request.user.is_authenticated:
                action = action
                productid = request.POST.get('productid', '')
                product = models.ProductModel.objects.get(pk=productid)
                pname = product.pname
                pprice = product.pprice
                pdescription = product.pdescription
                models.ProductModel.objects.filter(pk=productid).delete()
                return render(request, "operation.html", locals())
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'})

    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})


def usr_login(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        try:
            login(request, user)
            return redirect("operation")
        except:
            return redirect('login')
    elif not request.user.is_authenticated:
        return render(request, 'login.html')
    else:
        return HttpResponse('Login Failed')

def usr_logout(request):
    logout(request)
    # return HttpResponse('Logout Successful')
    return redirect('operation')

def usr_register(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            print('save')
            return redirect('login')  # 注册成功后重定向到登录页面
        else:
            print('form is not valid')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration.html', {'form': form})