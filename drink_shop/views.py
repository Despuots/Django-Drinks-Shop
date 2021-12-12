from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, View, TemplateView, CreateView
from django.utils import timezone
from .forms import CheckOutForm, AddCommentForm
from .models import Category, Product, OrderProduct, Order, Comment, ShippingAddress

from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

# Create your views here.


class HistoryView(LoginRequiredMixin, ListView):
    def get(self, *args, **kwargs):
        ordered_order = Order.objects.all().filter(user=self.request.user, ordered=True).order_by('-start_date')

        context = {
            'object_list': ordered_order
        }
        return render(self.request, 'user_history.html', context=context,)


class ProductView(ListView):
    model = Product
    template_name = "products.html"
    paginate_by = 24


class PaypalPayment(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            shipping_address = ShippingAddress.objects.get(user=self.request.user)

            context = {
                'order': order,
                'shipping_address': shipping_address
            }
            return render(self.request, 'paypal.html', context=context,)
        except ObjectDoesNotExist:
            return redirect("/")


class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckOutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)

    def post(self, *args, **kwargs):
        form = CheckOutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                delete_address = ShippingAddress.objects.get(user=self.request.user)
                delete_address.delete()
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                city = form.cleaned_data.get('city')
                postal_code = form.cleaned_data.get('postal_code')
                shipping_address = ShippingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    city=city,
                    postal_code=postal_code
                )
                shipping_address.save()
                order.save()
                return redirect('drink_shop:paypal')
            messages.warning(self.request, "Failed to checkout")
            return redirect('drink_shop:checkout')
        except ObjectDoesNotExist:
            return redirect("drink_shop:order_summary")


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context=context)
        except ObjectDoesNotExist:
            return redirect("/")


class ProductDetailView(DetailView):
    model = Product
    template_name = "product.html"


def product_by_category(request, slug):
    products = Product.objects.all().filter(category=slug)
    context = {
        'products': products,
    }
    return render(request, "product_by_category.html", context=context)


def featured_view(request):
    featured_categories = Category.objects.all().filter(featured=True, active=True)
    featured_products = Product.objects.all().filter(featured=True, active=True)
    context = {
        'featured_categories': featured_categories,
        'featured_products': featured_products,
    }
    return render(request, 'index.html', context=context)


@login_required
def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_product, created = OrderProduct.objects.get_or_create(product=product, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    print(order_qs)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
        else:
            order.products.add(order_product)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.products.add(order_product)
    return redirect("drink_shop:order-summary")


@login_required
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            order_product.quantity = 1
            order_product.save()
            order.products.remove(order_product)
            return redirect("drink_shop:order-summary")
        else:
            return redirect("drink_shop:product", slug=slug)
    else:
        return redirect("drink_shop:product", slug=slug)


@login_required
def remove_single_product_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product = OrderProduct.objects.filter(product=product, user=request.user, ordered=False)[0]
            if order_product.quantity > 1:
                order_product.quantity -= 1
                order_product.save()
            else:
                order.products.remove(order_product)
            return redirect("drink_shop:order-summary")
        else:
            return redirect("drink_shop:product", slug=slug)
    else:
        return redirect("drink_shop:product", slug=slug)


@login_required
def cart_cleaner(request):
    ordered_order = Order.objects.filter(user=request.user, ordered=False)[0]
    ordered_order.ordered = True
    ordered_order.ordered_date = datetime.now()
    ordered_order.save()

    ordered_products = OrderProduct.objects.all().filter(user=request.user, ordered=False)
    for order in ordered_products:
        order.ordered = True
        order.save()

    return redirect("drink_shop:order-summary")


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} already exist!')
                return redirect('drink_shop:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Email {email} already exist!')
                    return redirect('drink_shop:register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.success(request, 'Your registration was successful!')
                    return redirect('/accounts/login')
        else:
            messages.error(request, 'Passwords not matched!!')
            return redirect('drink_shop:register')
    return render(request, 'registration/register.html')


# class AddCommentView(CreateView):
#     def get(self, *args, **kwargs):
#         form = AddCommentForm()
#         context = {
#             'form': form
#         }
#         return render(self.request, context)
#
#     def post(self, request, *args, **kwargs):
#         return render(self.request)
