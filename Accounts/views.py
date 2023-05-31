from django.contrib import messages
from .models import CustomUserModel
from django.http import HttpResponse
from django.shortcuts import redirect , render
from Cart_Order.models import CartModel, CartItem
from django.contrib.auth import login, authenticate, logout
from Product.models import SizingModel, ColorsModel, ProductModel
from .forms import UserLoginForm, UserRegisterForm , EditUserForm
from django.contrib.auth.decorators import login_required
# Create your views here.


def user_register_view(request):
    if request.method == 'POST':
        path = request.GET.get('rd')
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = CustomUserModel()

            user.username = cd['username']
            user.email = cd['email']
            if len(cd['password1']) >= 8:
                if cd['password1'] == cd['password2']:
                    user.set_password(cd['password1'])
                    user.is_staff = False
                    user.is_superuser = False
                    user.save()
                    CartModel.objects.create(user=user)
                    messages.success(
                        request,
                        'حساب کاربری شما با موفقیت ایجاد شد . لطفا وارد شوید'
                    )
                    return redirect(path)
                else:
                    messages.error(
                        request,
                        'رمز عبور با تکرارش برابر نیست '
                    )
                    return redirect(path)
            else:
                messages.error(
                    request,
                    'رمز عبور کوتاه است . باید 8 رقم یا بیشتر باشد.'
                )
                return redirect(path)
        else:
            return HttpResponse('<h1 style="color:red"> Form Data False </h1>')
    else:
        return HttpResponse('<h1 style="color:red"> Bad Request </h1>')


def login_view(request):
    if request.method == 'POST':
        path = request.GET.get('rd')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            try:
                cart = request.session['Cart']
            except:
                cart = False

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(
                        request, f' {username}  عزیز شما وارد شدید')
                    if cart:
                        for item in cart:
                            cart_item = CartItem()
                            cart_item.color = ColorsModel.objects.get(name=item['color'])
                            cart_item.size = SizingModel.objects.get(size=item['size'])
                            cart_item.quantity = item['quantity']
                            cart_item.product = ProductModel.objects.get(id=item['product_id'])
                            cart_item.cart = request.user.cart()
                            cart_item.save()
                    return redirect(path)
                else:
                    return HttpResponse('<h1 style="color:red"> حساب کاربری شما فعال نمیباشد </h1>')
        else:
            return HttpResponse('<h1 style="color:red"> Form Data False </h1>')
    else:
        return HttpResponse('<h1 style="color:red"> Bad Request </h1>')


def logout_user(request):
    path = request.GET.get('rd')
    logout(request)
    messages.error(request, 'شما خارج شدید')
    return redirect(path)

@login_required(login_url='Main:Home') # type: ignore
def edit_user_view(request,pk):
    user = CustomUserModel.objects.get(id=pk)
    rd = request.GET.get('rd')
    if request.user == user :
        if (request.method == 'POST') and (request.user == user) :
            form = EditUserForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                user.first_name = cd['first_name']
                user.last_name = cd['last_name']
                user.email = cd['email']
                user.address = cd['address']
                user.address2 = cd['address2']
                user.postal_code = cd['postal_code']
                user.phone_number = cd['phone_number']
                user.save()
                messages.success(request,'اطلاعات ویرایش شده با موفقیت ثبت شد')
                return redirect(rd)
        else:
            form = EditUserForm()
            return render(request,'Accounts/edit_user.html',{'form': form, 'User': user})               
    else:
        return HttpResponse('<h1 style="color:red;"> 403 </h1>')    
