from django.shortcuts import render
from Product.models import ProductModel, SizingModel, ColorsModel, CategoriesModel
# Create your views here.


def home_view(request):
    products = ProductModel.objects.all()
    if not request.user.is_authenticated :
        cart = request.session.get('Cart', {})
    else:
        cart = False
        
    return render(request, 'index.html', {'Products': products, 'Cart': cart})


def search_view(request):
    if not request.user.is_authenticated :
        cart = request.session.get('Cart', {})
    else:
        cart = False

    if request.method == 'GET':
        key_word = request.GET.get('search')
        products = ProductModel.objects.filter(name__contains=key_word) | \
            ProductModel.objects.filter(description__contains=key_word)

        size = SizingModel.objects.all()
        colors = ColorsModel.objects.all()
        categories = CategoriesModel.objects.all()

        context = {
            'Products': products,
            'Sizes': size,
            'Colors': colors,
            'Categories': categories,
            'KeyWord': key_word,
            'Cart': cart,
        }
        return render(request, 'Product/shop-search.html', context)


def about_us_view(request):
    if not request.user.is_authenticated :
        cart = request.session.get('Cart', {})
    else:
        cart = False

    return render(request, 'Main/about-us.html', {'Cart': cart})


def contact_view(request):
    if not request.user.is_authenticated :
        cart = request.session.get('Cart', {})
    else:
        cart = False

    return render(request, 'Main/contact.html', {'Cart': cart})

# ! Errors Views


def err_404_view(request, exception):
    if not request.user.is_authenticated :
        cart = request.session.get('Cart', {})
    else:
        cart = False
        
    return render(request, 'Err/404.html',  {'Cart': cart})
