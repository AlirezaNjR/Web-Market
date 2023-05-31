from django.contrib import messages
from Cart_Order.models import CartItem
from Product.models import ProductModel
from rest_framework.response import Response
from Product.models import MultipleImageModel
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView, DestroyAPIView
from .serializers import CartItemSerializer
# Create your views here.


class CreateCartItemApiView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated,]

    def post(self, request, *args, **kwargs):

        cart = request.user.cart()

        quantity = request.POST.get('quantity')

        try:
            q = int(quantity)
            if q <= 0:
                return Response({'Detail': 'The quantity field value is invalid'}, 400)
        except:
            return Response({'Detail': 'The quantity field value is invalid'}, 400)

        try:
            product = ProductModel.objects.get(id=request.POST.get('product'))
        except ObjectDoesNotExist:
            return Response({'Detail': 'The product field value is invalid'}, 400)

        try:
            size = product.size.get(size=request.POST.get('size'))
        except ObjectDoesNotExist:
            return Response({'Detail': 'The size field value is invalid'}, 400)

        try:
            color = product.colors.get(name=request.POST.get('color'))
        except ObjectDoesNotExist:
            return Response({'Detail': 'The colors field value is invalid'}, 400)

        # ! If the number of choices is more than the number of inventory, it gives an error
        if int(quantity) > product.count:
            messages.error(
                request, f'تعداد بیش از حد مجاز . حد اکثر تعداد {product.count} عدد')
            return Response({'Detail': 'The number of selections is greater than the number in stock', 'Err': 'more'}, 400)

        try:  # ! If there is a product in the shopping cart, it will be added to its number
            item = CartItem.objects.get(
                product=product, size=size, color=color, cart=cart)

            # ! If the number of choices is more than the number of inventory, it gives an error
            if (int(item.quantity) + int(quantity)) > product.count:
                messages.error(
                    request, f'تعداد بیش از حد مجاز . حد اکثر تعداد {product.count} عدد')
                return Response({'Detail': 'The number of selections is greater than the number in stock', 'Err': 'more'}, 400)

            else:
                item.quantity = int(item.quantity) + int(quantity)
                item.save()

        except:
            item = CartItem.objects.create(
                product=product,
                quantity=quantity,
                size=size,
                color=color,
                cart=cart
            )

        messages.success(request, f'محصول {product.name} به سبد خرید اضافه شد')
        return Response(
            {
                'Detail': 'CartItem Created',
                'Banner': str(product.get_product_banner()),
                'Item_Id': item.pk,
            },
            201
        )


class CartItemDeleteView(DestroyAPIView):

    def destroy(self, request, *args, **kwargs):
        try:
            item = CartItem.objects.get(id=kwargs['pk'])
            if request.user.cart() == item.cart:
                item.delete()
                messages.error(
                    request, f'محصول {item.product.name} با موفقیت از سبد خرید حذف شد')
                return Response({'Detail': 'The item was removed from the shopping cart'}, 204)
            else:
                return Response({'Detail': 'You don\'t have access'}, 403)
        except ObjectDoesNotExist:
            return Response({'Detail': 'There is no item available'}, 400)

    permission_classes = [IsAuthenticated, ]


#!---------------------- Product Image --------------------
class DeleteProductImageView(DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            image = MultipleImageModel.objects.get(id=kwargs['pk'])
            if (image.uploader == request.user) or (request.user.is_superuser):
                image.delete_img()
                image.delete()
                return Response({'Detail': 'Image Deleted'}, 200)
            else:
                return Response({'Detail':'You don\'t have access'},403)
        except ObjectDoesNotExist:
            return Response({'Detail': 'Image not found'}, 404)
        
