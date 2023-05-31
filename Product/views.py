from django.contrib import messages
from django.http import HttpResponse
from .forms import CreateProductForm , EditProductForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import ProductModel, MultipleImageModel, CategoryModel, CategoriesModel, SizingModel, ColorsModel
# Create your views here.


def categories_view(request):
    categories = CategoriesModel.objects.all()
    return render(request, 'Product/category.html', {'Categories': categories})


def category_view(request, pk):
    category = CategoryModel.objects.filter(
        higher_category=get_object_or_404(CategoriesModel, id=pk))
    return render(request, 'Product/category.html', {'Categories': category, 'Create': True})


def product_create_view(request, pk):
    size = SizingModel.objects.all()
    colors = ColorsModel.objects.all()
    if (request.method == 'POST' ) and (request.user.is_superuser or request.user.is_staff):
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            product = ProductModel()
            product.name = cd['name']
            product.description = cd['description']
            product.user = request.user
            product.price = cd['price']
            product.count = cd['count']
            product.in_stock = (True if cd['in_stock']  else False)
            product.category = get_object_or_404(CategoryModel, id=pk)
            product.save()
            for color in cd['color']:
                
                product.colors.add(color.id)  
                
            for size in cd['size']:
                product.size.add(size.id)  
                
            product.save()
            [MultipleImageModel.objects.create(image=image, for_product=product, uploader=request.user)for image in request.FILES.getlist('image')]
            messages.success(
                request,
                f'محصول {product.name} با موفقیت ایجاد شد'
            )
            return redirect('Main:Home')
        else:
            return HttpResponse('<h1 style="color:red;"> 403 </h1>')
    else:
        form = CreateProductForm()
    return render(request, 'Product/create.html', {'form': form, 'Sizes': size, 'Colors': colors})


@login_required(login_url='Main:Home') # type: ignore
def product_edit_view(request, pk: int):
    product = get_object_or_404(ProductModel, id=pk)
    if (request.user == product.user) or (request.user.is_superuser):
        if request.method == 'POST':
            form = EditProductForm(request.POST,request.FILES)
            if form.is_valid():
                cd = form.cleaned_data
                product.name = cd['name']
                product.description = cd['description']
                product.user = request.user
                product.price = cd['price']
                product.count = cd['count']
                product.in_stock = (True if cd['in_stock'] else False)
                
                product.colors.clear()
                for color in cd['color']:
                    product.colors.add(color.id)  
                    
                product.size.clear()
                for size in cd['size']:
                    product.size.add(size.id)   
                
                [MultipleImageModel.objects.create(image=image, for_product=product, uploader=request.user)for image in request.FILES.getlist('image')]

                messages.success(request,f'{product.name}  با موفقیت  ویرایش  شد')
                product.save()
                return redirect(product.get_absolute_url())
        else:
            size = SizingModel.objects.all()
            color = ColorsModel.objects.all()
            form = EditProductForm()
            return render(request, 'Product/create.html', {'Product': product, 'form': form, 'Colors':color, 'Sizes': size})
    else:
        return HttpResponse('<h1 style="color:red;"> 403 </h1>')


def product_detail_view(request, pk: int):
    product = get_object_or_404(ProductModel, id=pk)
    if request.user.is_authenticated == False:
        cart = request.session.get('Cart', {})
    else:
        cart = False
    return render(request, 'Product/product.html', {"Product": product, 'Cart': cart})


def product_delete_view(request, pk: int):
    product = get_object_or_404(ProductModel, id=pk)
    if (request.user == product.user) or (request.user.is_superuser):
        [image.delete_img() for image in MultipleImageModel.objects.filter(for_product=product)]
        product.delete()
    else:
        return HttpResponse('<h1 style="color:red;"> 403 </h1>')
    return redirect('Main:Home')

#! ------------------ Image -------------------
@login_required(login_url='Main:Home') # type: ignore
def delete_image_view(request,pk):
    rd = request.GET.get('rd')
    image = get_object_or_404(MultipleImageModel,id=pk)
    if (image.uploader == request.user) or (request.user.is_superuser) :
        image.delete_img()
        image.delete()
        messages.success(request,f'{image}  با موفقیت حذف شد ')
        return redirect(rd)
    else:
        return HttpResponse('<h1 style="color:red;"> 403 </h1>')