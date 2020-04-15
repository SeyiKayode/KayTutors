from django.shortcuts import render, redirect, reverse
from .models import Membership, UserMembership, Subscription
from django.views.generic import ListView
from django.conf import settings
from django.contrib import messages
import stripe 
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def profile(request):
    user_membership = get_user_membership(request)
    user_subscription = get_user_subscription(request)
    context = {
        'user_membership': user_membership,
        'user_subscription': user_subscription
    }
    return render(request, 'memberships/profile.html', context)

def get_user_membership(request):
    user_membership_qs = UserMembership.objects.filter(user=request.user)
    if user_membership_qs.exists():
        return user_membership_qs.first()
    return None

def get_user_subscription(request):
    user_subscription_qs = Subscription.objects.filter(user_membership=get_user_membership(request))
    if user_subscription_qs.exists():
        user_subscription = user_subscription_qs.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type = request.session['selected_membership_type']
    selected_membership_qs = Membership.objects.filter(membership_type=membership_type)
    if selected_membership_qs.exists():
        return selected_membership_qs.first()
    return None

class MembershipList(ListView):
    model = Membership
    template_name = 'memberships/membership_list.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        current_membership = get_user_membership(self.request)
        context['current_membership'] = str(current_membership.membership)
        return context
    def post(self, request, **kwargs):
        selected_membership_type = request.POST.get('membership_type')
        user_membership = get_user_membership(request)
        user_subscription = get_user_subscription(request)
        selected_membership_qs = Membership.objects.filter(membership_type=selected_membership_type)
        if selected_membership_qs.exists():
            selected_membership = selected_membership_qs.first()
        if user_membership.membership == selected_membership:
            if user_subscription != None:
                messages.info(request, "You already have this membership. your next payment is due {}".format('get this value from stripe'))
                return redirect(request.META.get('HTTP_REFERER'))
        request.session['selected_membership_type'] = selected_membership.membership_type
        return redirect(reverse('memberships:payment'))

def PaymentView(request):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    publishKey = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            token = request.POST["stripeToken"]
            customer = stripe.Customer.retrieve(user_membership.stripe_customer_id)
            customer.source = token
            customer.save() 
            subscription = stripe.Subscription.create(customer=user_membership.stripe_customer_id, items=[
                {'plan': selected_membership.stripe_plan_id},
            ])
            return redirect(reverse('memberships:update-transactions', kwargs={
                'subscription_id': subscription.id
            }))
        except:
            messages.info(request, 'An error has occured')
    context = {
        'publishKey': publishKey,
        'selected_membership': selected_membership
    }
    return render(request, 'memberships/membership_payment.html', context)

def updateTransactions(request, subscription_id):
    user_membership = get_user_membership(request)
    selected_membership = get_selected_membership(request)
    user_membership.membership = selected_membership    
    user_membership.save()
    sub, created = Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id = subscription_id
    sub.active = True
    sub.save()
    try:
        del request.session['selected_membership_type']
    except:
        pass
    messages.info(request, "Successfully created {} membership".format(selected_membership))
    return redirect('/memberships')

def cancelSubscription(request):
    user_subscription = get_user_subscription(request)
    if user_subscription.active is False:
        messages.info(request, "You don't have an active membership")
        return redirect(request.META.get('HTTP_REFERER'))
    subscription = stripe.Subscription.retrieve(user_subscription.stripe_subscription_id)
    subscription.delete()
    user_subscription.active = False
    user_subscription.save()
    free_membership = Membership.objects.filter(membership_type='Free').first()
    user_membership = get_user_membership(request)
    user_membership.membership = free_membership
    user_membership.save()
    messages.info(request, "Successfully cancelled membership")
    return redirect('/memberships')
