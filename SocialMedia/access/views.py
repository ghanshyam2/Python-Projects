from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import RegistrationForm
from .tokens import account_activation_token
from users.models import Profile

User = get_user_model()


class Register(View, TemplateResponseMixin):
    form_class = RegistrationForm
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        user_email = request.POST.get("email")
        try:
            existing_user = User.objects.get(email=user_email)
            if not existing_user.is_active:
                existing_user.delete()
        except Exception:
            pass

        form = self.form_class(request.POST)
        if form.is_valid() is False:
            return self.render_to_response(context={"form": form})

        user = form.save()
        user.is_active = False
        user.save()

        current_site = get_current_site(request)  # 127.0.0.1:8000
        mail_subject = 'Activate your account.'
        message = render_to_string("active_email.html", {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = user.email

        try:
            send_mail(
                subject=mail_subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
                fail_silently=False
            )
            messages.success(request, "Link has been sent to your email id.")
        except Exception:
            form.add_error('', 'Error Occurred while Sending EMail, Try Again')
            messages.error(request, "Error occurred while sending mail")
            return self.render_to_response({'form': form})

        return HttpResponse("We have sent the verification email, please check your email inbox")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
        user = None

    if user is not None and account_activation_token.check_token(user, token) is True:
        user.is_active = True
        user.save()
        profile = Profile.objects.create(user=user)
        messages.success(request, "Successfully Verified")
        return redirect(reverse("login"))
    else:
        return HttpResponse("Activation link is invalid or your account is already verified! Try to login")


class LoginUserView(LoginView):
    template_name = "login.html"
    # success_url = reverse_lazy("home")

    # def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
    #     return super().post(request, *args, **kwargs)


class LogoutUserView(LogoutView):
    pass



#adminadmin - user_name
#Admin123456 - password


