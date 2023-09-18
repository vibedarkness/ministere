from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self,request,view_func,view_args,view_kwargs):
        modulename=view_func.__module__
        user=request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "users.HodViews":
                    pass
                elif modulename == "users.views":
                    pass
                else:
                    return HttpResponse("admin")
            elif user.user_type == "2":
                if modulename == "users.StaffViews":
                    pass
                elif modulename == "users.views":
                    pass
                else:
                    return HttpResponse("staff")

        else:
            if request.path == reverse("show_login") or request.path == reverse("do_login"):
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))