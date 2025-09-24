from django.shortcuts import render , redirect
from django.contrib import messages , auth
from .forms import RegisterForm
from .models import Account
from django.contrib.auth.decorators import login_required

# send email neede...
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage



# ------Register------ #

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            email        = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password     = form.cleaned_data['password']
            user_name    = email.split('@')[0]
            user = Account.objects.create_user(first_name = first_name , last_name = last_name,email = email ,username=user_name , password =password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Please Avtivate Your Account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user' : user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message , to = [to_email])
            send_email.send()
            return redirect('/accounts/login/?commend=verification&email='+email)
        
    else:
        form = RegisterForm()
    context = {'form' : form ,}

    return render(request , 'accounts/register.html' , context)

# ------Login------ #

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email = email , password = password)

        if user is not None :
            auth.login(request , user)
            return redirect('home')
        else : 
            messages.error(request , ' Invalid Credential.')
            return redirect('login')
    return render(request , 'accounts/login.html')

# ------Logout------ #

@login_required(login_url= 'login')
def logout(request):
    auth.logout(request)
    messages.success(request , 'you are successfully logged out!')
    return redirect('login')

# ------Register Active------ #

def activate(request , uidb64 , token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)
    except(TypeError , ValueError , OverflowError , Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user ,token):
        user.is_active = True
        user.save()
        messages.success(request , 'Your Account is Activated!')
        return redirect('login')
    else:
        messages.error(request , 'Invalid Activation..')
        return redirect('register')