import traceback
import random
import logging
import pytz

# Setup logging
logger = logging.getLogger(__name__)


def booleanize(*args, **kwargs):
    # Handle both single value and kwargs to get arg name
    name = None
    if args and not kwargs:
        value=args[0]
    elif kwargs and not args:
        for item in kwargs:
            name  = item
            value = kwargs[item]
            break
    else:
        raise Exception('Internal Error')

    # Handle shortcut: an arg with its name equal to ist value is considered as True
    if name==value:
        return True

    if isinstance(value, bool):
        return value
    else:
        if value.upper() in ('TRUE', 'YES', 'Y', '1'):
            return True
        else:
            return False


def timezonize(timezone):
    '''Convert a string representation of a timezone to its pytz object or do nothing if the argument is already a pytz timezone'''
    if not 'pytz' in str(type(timezone)):
        timezone = pytz.timezone(timezone)
    return timezone


def send_email(to, subject, text):

    # Importing here instead of on top avoids circular dependencies problems when loading booleanize in settings
    from django.conf import settings

    if settings.DJANGO_EMAIL_SERVICE == 'Sendgrid':
        import sendgrid
        from sendgrid.helpers.mail import Email,Content,Mail

        sg = sendgrid.SendGridAPIClient(apikey=settings.DJANGO_EMAIL_APIKEY)
        from_email = Email(settings.DJANGO_EMAIL_FROM)
        to_email = Email(to)
        subject = subject
        content = Content('text/plain', text)
        mail = Mail(from_email, subject, to_email, content)

        try:
            response = sg.client.mail.send.post(request_body=mail.get())
            #logger.debug(response.status_code)
            #logger.debug(response.body)
            #logger.debug(response.headers)
        except Exception as e:
            logger.error(e)

        #logger.debug(response)


def format_exception(e):

    # Importing here instead of on top avoids circular dependencies problems when loading booleanize in settings
    from django.conf import settings

    if settings.DEBUG:
        # Cutting away the last char removed the newline at the end of the stacktrace 
        return str('Got exception "{}" of type "{}" with traceback:\n{}'.format(e.__class__.__name__, type(e), traceback.format_exc()))[:-1]
    else:
        return str('Got exception "{}" of type "{}" with traceback "{}"'.format(e.__class__.__name__, type(e), traceback.format_exc().replace('\n', '|')))


def log_user_activity(level, msg, request, caller=None):

    # Get the caller function name through inspect with some logic
    #import inspect
    #caller =  inspect.stack()[1][3]
    #if caller == "post":
    #    caller =  inspect.stack()[2][3]

    try:
        msg = str(caller) + " view - USER " + str(request.user.email) + ": " + str(msg)
    except AttributeError:
        msg = str(caller) + " view - USER UNKNOWN: " + str(msg)

    try:
        level = getattr(logging, level)
    except:
        raise

    logger.log(level, msg)


def random_username():
    '''Create a random string of 156 chars to be used as username'''             
    username = ''.join(random.choice('abcdefghilmnopqrtuvz') for _ in range(16))
    return username

