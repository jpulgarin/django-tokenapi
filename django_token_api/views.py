from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from api.tokens import default_token_generator
from django.contrib.auth import authenticate, login
from django.contrib.sites.models import Site
from django.views.decorators.cache import never_cache

from datetime import date, datetime

from emailauth.forms import RegistrationForm
from emailauth.models import UserEmail

from sorl.thumbnail import get_thumbnail

from loyalti.models import *
from loyalti.forms import *
from loyalti.constants import * 

try: 
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps # Python 2.4 fallback

try: 
    import simplejson as json
except ImportError: 
    import json


# Decorator for using API with normal auth vs token
def logged_in_or_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'token' in request.REQUEST and \
            'user' in request.REQUEST:
                user = authenticate(pk=request.REQUEST['user'], token=request.REQUEST['token'])
                if user:
                    login(request, user)
                    return view_func(request, *args, **kwargs)
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)
        
        return HttpResponseForbidden()
    return _wrapped_view


# JSON helper functions
def JSONResponse(data, dump=True):
    return HttpResponse(
        json.dumps(data) if dump else data,
        mimetype='application/json',
    )

def JSONError(error_string):
    data = {
        'success': False,
        'errors': error_string,
    }
    return JSONResponse(data)


# Loyalti API
# ":parameter" means the URL parameter is required
# "<parameter>" means the URL parameter is optional

# GET API

# token/:token.json
# Required: user
# Returns: success&error
# TODO: Add a message mechanism here to be able to display messages to user 
# on app startup.
@never_cache
def token(request, token):
    if 'user' in request.GET:
        data = {}

        try:
            user = User.objects.get(pk=request.GET['user'])
        except User.DoesNotExist:
            return JSONError("User does not exist.")
        if default_token_generator.check_token(user, 
            token): 
            try:
                email = UserEmail.objects.get(user=user)
                # Only allow unverified logins for 24 hours
                if not email.verified and \
                    (datetime.now() - user.date_joined).days >= 1:
                    return HttpResponseForbidden()
            except UserEmail.DoesNotExist:
                pass
            data['success'] = True
        else:
            return JSONError("Token did not match user.")
        return JSONResponse(data)

# points.json
# Returns: 
@logged_in_or_token
@never_cache
def points(request):
    if request.method == 'GET':
        data = []

        points = request.user.points_set.all()
        today = date.today()
        for point in points:
            rewards_queryset = Reward.objects.filter(store=point.store,
                start__lte=today, end__gte=today)
            rewards = []
            date_format = "%b %d"
            for r in rewards_queryset:
                rewards.append({
                    'pk' : r.pk,
                    'title': r.title,
                    'description': r.description,
                    'points_required': r.points_required,
                    'start': r.start.strftime(date_format),
                    'end': r.end.strftime(date_format),
                })
            
            data.append({
                'name': point.store.name,
                'logo': get_thumbnail(point.store.logo, '80', 
                    crop='center', quality=99).url,
                'points': point.points,
                'rewards': rewards,
            })
        return JSONResponse(data)


# POST API

# token_new.json
# IMPORTANT TODO: This should go over SSL.
# Required: username&password
# Returns: token&user
@never_cache
def token_new(request):
    if request.method == 'POST':
        if 'username' in request.POST and 'password' in request.POST:
            user = authenticate(username=request.POST['username'], 
                password=request.POST['password'])
            if user:
                try:
                    email = UserEmail.objects.get(user=user)
                    # Only allow unverified logins for 24 hours
                    if not email.verified and \
                        (datetime.now() - user.date_joined).days >= 1:
                        return JSONError("You need to verify your email before logging in again.")
                except UserEmail.DoesNotExist:
                    pass
                data = {}
                data['success'] = True
                data['token'] = default_token_generator.make_token(user)
                data['user'] = user.pk
                data['username'] = user.username
                return JSONResponse(data)
            else:
                return JSONError("Unable to log you in, please try again")

# signup.json
# IMPORTANT TODO: This should go over SSL.
# Required: first_name&last_name&password1&password2&email
# &country
@never_cache
def signup(request):
    if request.method == 'POST':
        data =  {}

        f = RegistrationForm(request.POST)
        if f.is_valid(): 
            fields = f.cleaned_data
            email = UserEmail.objects.create_unverified_email(
                fields['email'])
            email.send_verification_email()

            user = User()
            user.is_active = False
            user.email = email.email
            user.set_password(fields['password1'])
            user.username = fields['username']
            user.save()
            
            # Set user profile
            profile = user.get_profile()
            profile.save()

            email.user = user

            email.save()

            data['success'] = True
            data['user'] = user.pk
            data['token'] = default_token_generator.make_token(user)
            data['username'] = user.username
        else:
            return JSONError(f.errors)
        return JSONResponse(data)

# transaction/new.json
# Required: secret
@logged_in_or_token
@never_cache
def transaction_new(request):
    if request.method == 'POST':
        data = {}

        fields = request.POST.copy()
        fields['customer'] = request.user.pk
        try: 
            fields['secret'] = Secret.objects.get(
                secret_string=fields['secret']).pk
        except Secret.DoesNotExist:
            return JSONError("Unable to process transaction, please try again.")
        f = TransactionForm(fields)
        try:
            transaction = f.save()
            store = transaction.secret.batch.store
            # TODO test this
            if not store:
                transaction.delete()
                return JSONError("This booklet has not yet been activated.")
            gain = 1
            try:
                points = Points.objects.get(user=request.user, store=store)
                points.points += gain
            except Points.DoesNotExist:
                points = Points(user=request.user, store=store)
                points.points = gain
            points.save()
            data['points'] = points.points
            data['gain'] = gain
            data['logo'] = get_thumbnail(store.logo, '80', 
                crop='center', quality=99).url
            data['name'] = store.name
            data['success'] = True
        except ValueError:
            return JSONError(f.errors)
        return JSONResponse(data);

# redemption/new.json
# Required: pk
@logged_in_or_token
@never_cache
def redemption_new(request):
    if request.method == 'POST':
        data = {}

        if 'pk' in request.POST and 'secret' in request.POST:
            try: 
                reward = Reward.objects.get(pk=request.POST['pk'])
            except Reward.DoesNotExist:
                return JSONError("This reward no longer exists, sorry!")

            today = date.today()
            if reward.start > today:
                return JSONError("Reward is not valid yet.")
            if reward.end < today:
                return JSONError("Reward has expired.")

            try: 
                store = Store.objects.get(secret_string=request.POST['secret'])
            except Store.DoesNotExist:
                return JSONError("QR code did not match any store")

            if not store == reward.store:
                return JSONError("QR code does not match reward")

            try:
                points = Points.objects.get(user=request.user, 
                    store=reward.store)
            except Points.DoesNotExist:
                return JSONError("You do not have any points at this store!")

            if points.points <  reward.points_required:
                return JSONError("You do not have sufficient points to claim \
                    this reward.")
    
            redemption = Redemption(reward=reward, customer=request.user)
            redemption.save()
            points.points -= reward.points_required
            points.save()

            data['success'] = True
            data['response_string'] = store.response_string
            data['store'] = store.name
            data['reward'] = reward.title
            data['points_required'] = reward.points_required
            data['points'] = points.points
            return JSONResponse(data);
