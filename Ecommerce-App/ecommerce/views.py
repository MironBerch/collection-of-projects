import random
import string
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .forms import CheckoutForm, CouponForm, RefundForm, PaymentForm
from .models import Item, OrderItem, Order, Address, Payment, Coupon, Refund, UserProfile
from ecommerce.forms import SignupForm
from django.contrib.auth.models import User


stripe.api_key = settings.STRIPE_SECRET_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    items = Item.objects.all()
    
    context = {
        'items': items,
    }

    return render(request, 'products.html', context)



def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST or None)
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get('use_default_shipping')
                if use_default_shipping:
                    address_qs = Address.objects.filter(
                        user=request.user, address_type='S', default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            request, 'No default shipping address available')
                        return redirect('checkout')
                else:
                    shipping_address1 = form.cleaned_data.get('shipping_address')
                    shipping_address2 = form.cleaned_data.get('shipping_address2')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_zip]):
                        shipping_address = Address(
                            user=request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()
                        set_default_shipping = form.cleaned_data.get('set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get('use_default_billing')
                same_billing_address = form.cleaned_data.get('same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    address_qs = Address.objects.filter(
                        user=request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(request, 'No default billing address available')
                        return redirect('core:checkout')
                else:
                    print('User is entering a new billing address')
                    billing_address1 = form.cleaned_data.get('billing_address')
                    billing_address2 = form.cleaned_data.get('billing_address2')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_zip]):
                        billing_address = Address(
                            user=request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                        set_default_billing = form.cleaned_data.get('set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(request, 'Please fill in the required billing address fields')

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'S':
                    return redirect('payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('payment', payment_option='paypal')
                else:
                    messages.warning(request, 'Invalid payment option selected')
                    return redirect('checkout')
        except ObjectDoesNotExist:
            messages.warning(request, 'You do not have an active order')
            return redirect('order-summary')

    if request.method == 'GET':
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            form = CheckoutForm()

            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': True
            }

            shipping_address_qs = Address.objects.filter(
                user=request.user, address_type='S', default=True
            )

            if shipping_address_qs.exists():
                context.update({'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=request.user, address_type='B', default=True
            )

            if billing_address_qs.exists():
                context.update({'default_billing_address': billing_address_qs[0]})

            return render(request, 'checkout.html', context)
        
        except ObjectDoesNotExist:
            messages.info(request, 'You do not have an active order')
            return render('checkout')


def payment_view(request):
    if request.method == 'GET':
        order = Order.objects.get(ser=request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'STRIPE_PUBLIC_KEY' : settings.STRIPE_PUBLIC_KEY
            }
            userprofile = request.user.userprofile
            if userprofile.one_click_purchasing:
                cards = stripe.Customer.list_sources(
                    userprofile.stripe_customer_id, limit=3, object='card'
                )
                card_list = cards['data']
                if len(card_list) > 0:
                    context.update({'card': card_list[0]})
            return render(request, 'payment.html', context)
        else:
            messages.warning(request, 'You have not added a billing address')
            return redirect('checkout')

    if request.method == 'POST':
        order = Order.objects.get(user=request.user, ordered=False)
        form = PaymentForm(request.POST)
        userprofile = UserProfile.objects.get(user=request.user)
        if form.is_valid():
            token = form.cleaned_data.get('stripeToken')
            save = form.cleaned_data.get('save')
            use_default = form.cleaned_data.get('use_default')

            if save:
                if userprofile.stripe_customer_id != '' and userprofile.stripe_customer_id is not None:
                    customer = stripe.Customer.retrieve(userprofile.stripe_customer_id)
                    customer.sources.create(source=token)
                else:
                    customer = stripe.Customer.create(email=request.user.email)
                    customer.sources.create(source=token)
                    userprofile.stripe_customer_id = customer['id']
                    userprofile.one_click_purchasing = True
                    userprofile.save()

            amount = int(order.get_total() * 100)

            try:
                if use_default or save:
                    charge = stripe.Charge.create(
                        amount=amount, currency='usd', customer=userprofile.stripe_customer_id
                    )
                else:
                    charge = stripe.Charge.create(
                        amount=amount, currency='usd', source=token
                    )

                payment = Payment()
                payment.stripe_charge_id = charge['id']
                payment.user = request.user
                payment.amount = order.get_total()
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()
                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code
                order.save()

                messages.success(request, 'Your order was successful!')
                return redirect('/')
            
            except stripe.error.CardError as e:
                body = e.json_body
                err = body.get('error', {})
                messages.warning(request, f"{err.get('message')}")
                return redirect('/')

            except stripe.error.StripeError as e:
                messages.warning(request, 'Something went wrong. You were not charged. Please try again.')
                return redirect('/')

            except Exception as e:
                messages.warning(request, 'A serious error occurred. We have been notifed.')
                return redirect('/')

        messages.warning(request, 'Invalid data received')
        return redirect('/payment/stripe/')


def home_view(request):
    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'home.html', context)


def order_summary_view(request):
    if request.method == 'GET':
        try:
            order = Order.objects.get(user=request.user, ordered=False)

            context = {
                'order': order,
            }

            return render(request, 'order_summary.html', context)

        except ObjectDoesNotExist:
            messages.warning(request, 'You do not have an active order')
            return redirect('/')


def item_detail_view(request, slug):
    item = Item.objects.filter(title=slug)

    context = {
        'item': item,
    }

    return render(request, 'product.html', context)


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item, user=request.user, ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated.')
            return redirect('order-summary')
        else:
            order.items.add(order_item)
            messages.info(request, 'This item was added to your cart.')
            return redirect('order-summary')
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date
        )
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart.')
        return redirect('order-summary')


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_qs.exists():
        order = order.qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, 'This item was removed from your cart.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('product', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product', slug=slug)



@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user, ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item, user=request.user, ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'This item quantity was updated.')
            return redirect('order-summary')
        else:
            messages.info(request, 'This item was not in your cart')
            return redirect('product', slug=slug)
    else:
        messages.info(request, 'You do not have an active order')
        return redirect('product', slug=slug)


def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'This coupon does not exist')
        return redirect('checkout')


def add_coupon_view(request):
    if request.method == 'POST':
        form = CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=request.user, ordered=False
                )
                order.coupon = get_coupon(request, code)
                order.save()
                messages.success(request, 'Successfully added coupon')
                return redirect('checkout')
            except ObjectDoesNotExist:
                messages.info(request, 'You do not have an active order')
                return redirect('checkout')


def request_refund_view(request):
    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get('ref_code')
            message = form.cleaned_data.get('message')
            email = form.cleaned_data.get('email')

            try:
                order = Order.objects.get(ref_code=ref_code)
                order.refund_requested = True
                order.save()

                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.info(request, 'Your request was received.')
                return redirect('request-refund')

            except ObjectDoesNotExist:
                messages.info(request, 'This order does not exist.')
                return redirect('request-refund')

    if request.method == 'GET':
        form = RefundForm()

        context = {
            'form': form,
        }

        return render(request, 'request_refund.html', context)


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('login')
	else:
		form = SignupForm()
	context = {
		'form':form,
	}
	return render(request, 'account/signup.html', context)