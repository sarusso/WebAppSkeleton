import uuid
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.models import User
from .models import Profile, LoginToken
from .utils import send_email, format_exception, timezonize
from .decorators import public_view, private_view
from .exceptions import ErrorMessage

# Setup logging
import logging
logger = logging.getLogger(__name__)


@public_view
def login_view(request):

    data = {}

    # If authenticated user reloads the main URL
    if request.method == 'GET' and request.user.is_authenticated:
        return HttpResponseRedirect('/')

    # If unauthenticated user tries to log in
    if request.method == 'POST':
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            # Use Django's machinery to attempt to see if the username/password
            # combination is valid - a User object is returned if it is.

            if "@" in username:
                # Get the username from the email
                try:
                    user = User.objects.get(email=username)
                    username = user.username
                except User.DoesNotExist:
                    if password:
                        raise ErrorMessage('Check email and password')
                    else:
                        # Return here, we don't want to give any hints about existing users
                        data['success'] = 'Ok, if we have your data you will receive a login link by email shortly.'
                        return render(request, 'success.html', {'data': data})

            if password:
                if user.profile.auth != 'local':
                    # This actually hides that the user cannot be authenticated using the local auth.
                    raise ErrorMessage('Check email and password')
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    response = HttpResponseRedirect('/')
                    response.delete_cookie('post_login_redirect')
                    return response
                else:
                    raise ErrorMessage('Check email and password')
            else:

                # If empty password and local auth, send mail with login token
                if user.profile.auth == 'local':

                    logger.debug('Sending login token via mail to {}'.format(user.email))

                    token = uuid.uuid4()

                    # Create token or update if existent (and never used)
                    try:
                        loginToken = LoginToken.objects.get(user=user)
                    except LoginToken.DoesNotExist:
                        LoginToken.objects.create(user=user, token=token)
                    else:
                        loginToken.token = token
                        loginToken.save()
                    try:
                        send_email(to=user.email, subject='Web App login link', text='Hello,\n\nhere is your login link: https://{}/login/?token={}\n\nOnce logged in, you can go to "My Account" and change password (or just keep using the login link feature).\n\nThe Web App Team.'.format(settings.PUBLIC_HOST, token))
                    except Exception as e:
                        logger.error(format_exception(e))
                        raise ErrorMessage('Something went wrong. Please retry later.')

                    # Return here, we don't want to give any hints about existing users
                    data['success'] = 'Ok, if we have your data you will receive a login link by email shortly.'
                    return render(request, 'success.html', {'data': data})


        else:
            # This should never happen: user tried to log-in while already logged in: log him out and then render the login
            logout(request)

    else:
        # If we are logging in through a token
        token = request.GET.get('token', None)

        if token:

            loginTokens = LoginToken.objects.filter(token=token)

            if not loginTokens:
                raise ErrorMessage('Token not valid or expired')


            if len(loginTokens) > 1:
                raise Exception('Consistency error: more than one user with the same login token ({})'.format(len(loginTokens)))

            # Use the first and only token (todo: use the objects.get and correctly handle its exceptions)
            loginToken = loginTokens[0]

            # Get the user from the table
            user = loginToken.user

            # Set auth backend
            user.backend = 'django.contrib.auth.backends.ModelBackend'

            # Ok, log in the user
            login(request, user)
            loginToken.delete()

            # Now redirect to site
            response = HttpResponseRedirect('/')
            response.delete_cookie('post_login_redirect')
            return response

    # All other cases, render the login page again with no other data than title
    return render(request, 'login.html', {'data': data})


@private_view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


@public_view
def register_view(request):

    data = {}

    # If authenticated user reloads the main URL
    if request.method == 'GET' and request.user.is_authenticated:
        return HttpResponseRedirect('/main/')

    # If unauthenticated register if post
    if request.method == 'POST':
        if not request.user.is_authenticated:
            email    = request.POST.get('email')
            password = request.POST.get('password')
            invitation = request.POST.get('invitation')

            if settings.INVITATION_CODE:
                if invitation != settings.INVITATION_CODE:
                    raise ErrorMessage('Wrong invitation code')

            if '@' not in email:
                raise ErrorMessage('Detected invalid email address')

            # Register the user
            user = User.objects.create_user(random_username(), password=password, email=email)
            user.save()
            data['user'] = user

            # Create the profile
            logger.debug('Creating user profile for user "{}"'.format(user.email))
            Profile.objects.create(user=user)

            # Manually set the auth backend for the user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            data['status'] = 'activated'

    # All other cases, render the login page again with no other data than title
    return render(request, 'register.html', {'data': data})


@public_view
def entrypoint_view(request):
    return HttpResponseRedirect('/main/')


@public_view
def main_view(request):
    return render(request, 'main.html', {'data': {}})


@private_view
def account_view(request):

    data={}
    data['user'] = request.user

    # Get & set profile
    profile = Profile.objects.get(user=request.user)
    data['profile'] = profile

    # Set values from POST and GET
    edit = request.POST.get('edit', None)
    if not edit:
        edit = request.GET.get('edit', None)
        data['edit'] = edit
    value = request.POST.get('value', None)

    # Fix None
    if value and value.upper() == 'NONE':
        value = None
    if edit and edit.upper() == 'NONE':
        edit = None

    # Edit values
    if edit and value:
        try:
            logger.info('Setting "{}" to "{}"'.format(edit,value))

            # Timezone
            if edit=='timezone' and value:

                # Validate & save
                timezonize(value)
                profile.timezone = value
                profile.save()

            # Email
            elif edit=='email' and value:
                request.user.email=value
                request.user.save()

            # Password
            elif edit=='password' and value:
                # If no local auth, you should never get here
                if request.user.profile.auth != 'local':
                    raise ErrorMessage('Cannot change password using an external authentication service')
                request.user.set_password(value)
                request.user.save()

            # Generic property
            elif edit and value:
                raise Exception('Attribute to change is not valid')

        except Exception as e:
            logger.error(format_exception(e))
            data['error'] = 'The property "{}" does not exists or the value "{}" is not valid.'.format(edit, value)
            return render(request, 'error.html', {'data': data})

    return render(request, 'account.html', {'data': data})
