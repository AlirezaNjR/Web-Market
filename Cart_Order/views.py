from .models import CartItem
from datetime import datetime
from .forms import OrderInfoForm
from django.contrib import messages
from django.http import HttpResponse
from Product.models import ProductModel
from Accounts.models import CustomUserModel
from .models import OrderItemModel, OrderModel 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect , get_object_or_404 , get_list_or_404
# Create your views here.


def cart_item_to_session(
    request,name:str,color:str,size:str,
    id:str,quantity:str,image:str,url:str) -> None :
    try:
        cart = list(request.session['Cart'])
        added = False
        for item in cart:  #! If there is a product in the shopping cart, it will be added to its number
            if (item["name"] == name) and (item["color"] == color) and (item["size"] == size) : 
                item['quantity'] = int(quantity) + int(item['quantity'])
                added = True
        if added == False:
            cart.append(
                {
                    'name': name,
                    'color': color,
                    'size': size,
                    'product_id': id,
                    'quantity': quantity,
                    'image': image,
                    'url': url,
                }
            )
        request.session['Cart'] = cart
        
    except:
        request.session['Cart'] = [
            {
                'name': name,
                'color': color,
                'size': size,
                'product_id': id,
                'quantity': quantity,
                'image': image,
                'url': url,
            }
        ]


def add_to_cart_view(request):
    rd = request.GET.get('rd')
    if request.method == 'POST':
        #! Adds item in cart for logged users
        if request.user.is_authenticated :
            quantity = request.POST.get('quantity')
            product = ProductModel.objects.get(id=request.POST.get('product'))
            color = product.colors.get(name=request.POST.get('color'))
            
            if int(quantity) > product.count : #! If the number of choices is more than the number of inventory, it gives an error
                messages.error(request,f'تعداد بیش از حد مجاز . حد اکثر تعداد {product.count} عدد')
                return redirect(product.get_absolute_url())
            
            cart = request.user.cart()
            size = product.size.get(size=request.POST.get('size'))
            
            try :  #! If there is a product in the shopping cart, it will be added to its number
                item = CartItem.objects.get(product=product, size=size, color=color, cart=cart)
                
                if (int(item.quantity) + int(quantity)) > product.count : #! If the number of choices is more than the number of inventory, it gives an error 
                    messages.error(request,f'تعداد بیش از حد مجاز . حد اکثر تعداد {product.count} عدد')
                    return redirect(product.get_absolute_url())
                
                else:
                    item.quantity = int(item.quantity) + int(quantity)
                    item.save()
            
            except:
                CartItem.objects.create(product=product, quantity=quantity, size=size, color=color, cart=cart)
            
            messages.success(request, f' محصول {product.name} به سبد خرید اضافه شد ')
            return redirect(product.get_absolute_url())
        
        elif request.user.is_authenticated == False :
            #! Adds item in session for anonymous users
            cart_item_to_session(
                request = request,
                name = request.GET.get('p_name'),
                color = request.POST.get('color'),
                size = request.POST.get('size'),
                id = request.POST.get('product'),
                quantity = request.POST.get('quantity'),
                image = request.GET.get('img'),
                url =  request.GET.get('p_url'),
                )
            
            messages.success(request,f' محصول  به سبد خرید اضافه شد ')
            return redirect(rd)


def delete_cart_item_view(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        rd = request.GET.get('rd')
        #! Removing item from cart for logined users 
        if request.user.is_authenticated : 
            item = CartItem.objects.get(id=id)
            
            if request.user == item.cart.user:
                item.delete()
                messages.error(request, f' محصول {item.product.name} از سبد خرید حذف شد.')
                return redirect(rd)
           
            else:
                return HttpResponse('<h1 style="color:red;">403</h1>')
        
        else :
            #! Removing item from session for anonymous users (not logged in yet)
            color = request.GET.get('color')
            size = request.GET.get('size')
            
            try: 
                cart = list(request.session['Cart'])
                
                for item in cart:
                    if (item['color'] == color) and (item['size'] == size) and (item['product_id'] == id):
                        cart.remove(item) 
                        request.session['Cart'] = cart
                        messages.error(request, f' محصول {item["name"]} از سبد خرید حذف شد.')
                        return redirect(rd)
            
            except:
                return redirect(rd)
    
    else:
        return HttpResponse('<h1 style="color:red;"> Bad Request </h1>')

    return render(request, 'Err/404.html')


#! --------------------- Oreder Views ---------------
@login_required(login_url='Main:Home') # type: ignore
def order_checkout_step_1(request):
    if str(request.user.cart_item()) != '<QuerySet []>':
        return render(request, 'Order/checkout-step-1.html')
    
    else:
        return redirect('Main:Home')


@login_required(login_url='Main:Home') # type: ignore
def order_checkout_step_2(request):
    if str(request.user.cart_item()) != '<QuerySet []>':
        
        if request.method == 'POST':
            form = OrderInfoForm(request.POST)
            
            if form.is_valid(): #! Saving Order information in Order Model
                order = OrderModel()
                cd = form.cleaned_data
                order.name = f'{cd["name"]} {cd["family"]}'
                order.address1 = cd['address1']
                order.address2 = cd['address2']
                order.user = request.user
                order.email = request.user.email
                order.phone = cd['phone']
                order.postal_code = cd['postal_code']
                order.total_price = request.user.cart().total_price()
                order.status = 'wait'
                order.save()
                #! Cart Items --> Order Items
                for item in request.user.cart_item():
                    order_item = OrderItemModel()
                    order_item.name = item.product.name
                    order_item.color = str(item.color)
                    order_item.size = str(item.size)
                    order_item.order_amount = item.quantity
                    order_item.price = item.item_price()
                    order_item.product = item.product
                    order_item.order = order
                    order_item.save()
                return redirect('Cart_Order:Order_Checkout_3', order.pk)
            else:
                pass
        else:
            form = OrderInfoForm()
            
        return render(request, 'Order/checkout-step-2.html', {'form': form})
    else:
        return redirect('Main:Home')
    
    
@login_required(login_url='Main:Home') # type: ignore
def order_checkout_step_3(request, pk): 
    if str(request.user.cart_item()) != '<QuerySet []>':
        #! Change order status to paid after payment 
        order = OrderModel.objects.get(id=pk)
        
        if (request.method == 'POST') and (order.status == 'wait') and (request.user == order.user):
            order.status = 'paid'
            order.tracking_number = order.pk
            order.pay_time = datetime.now()
            order.save()
            
            for item in order.OrderItem.all():  # type: ignore
                product = item.product
                product.count -= item.order_amount
                product.save()
            
            request.user.cart().clear_cart() #! All items in the  cart after purchase deletes 
            return redirect('Cart_Order:Order_Checkout_4', order.pk)
       
        #else:
        #    return HttpResponse('<h1 style="color:red;">403</h1>')
        
        return render(request,'Order/checkout-step-3.html')
    else:
        return redirect('Main:Home')
    
    
@login_required(login_url='Main:Home') # type: ignore
def order_checkout_step_4(request, pk):
    order = OrderModel.objects.get(id=pk)
    
    if order.status == 'paid':
        order_items = order.OrderItem.all()  # type: ignore
        return render(request, 'Order/checkout-step-4.html', {'Items': order_items, 'Order': order})
   
    else:
        messages.error(request,f'خطا در پرداخت سفارش {order.pk}')
        return redirect('Main:Home')
    
    
@login_required(login_url='Main:Home') # type: ignore
def order_cancell_view(request):
    pk = request.GET.get('pk')
    order = get_object_or_404(OrderModel, id=pk) 
    
    if (request.method == "GET") and (request.user == order.user) and (order.status == 'wait'):
        order.status = 'cancelled'
        order.save()
        return redirect('Cart_Order:User_Orders',pk=request.user.id)
    
    else:
        return HttpResponse('<h1 style="color:red;">403</h1>')
    
    
#! ------------------ User Orders ----------------------
@login_required(login_url='Main:Home')
def user_order_list_view(request,pk):
    user = get_object_or_404(CustomUserModel,id=pk)
    orders = OrderModel.objects.filter(user=user)
    
    if orders:
        
        if request.user == orders.first().user : # type: ignore
            return render(request, 'Order/user_order_list.html', {'Orders': orders})
        
        else:
            return HttpResponse('<h1 style="color:red;">403</h1>')
    
    else:
        return render(request,'Err/404.html')


@login_required(login_url='Main:Home') # type: ignore
def user_order_detail_view(request,pk):
    order = get_object_or_404(OrderModel,id=pk)
    if order.user == request.user :
        return render(request, 'Order/user_order_detail.html', {'Order': order})
    else:
        return HttpResponse('<h1 style="color:red;">403</h1>')