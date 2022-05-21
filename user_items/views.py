from time import sleep

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from core import utils

import items.services as item_services
import profiles.services as profiles_services
from user_items import services


# Create your views here.
class ListItems(View, LoginRequiredMixin):

    template_name = 'list-items.html'

    def _context(self, request: HttpRequest) -> dict:
        profile = profiles_services.profile_from_request(request)
        return {'user_items': services.list_items(profile), 'items': services.list_not_user_items(profile)}

    def get(self, request: HttpRequest):
        return render(request, self.template_name, self._context(request))

    def post(self, request: HttpRequest):
        form = utils.pop_csrf(request.POST)
        profile = profiles_services.profile_from_request(request)
        item = item_services.get_or_create(form['name'])
        services.create_user_item(profile, item)
        return render(request, self.template_name, self._context(request))


class CreateItem(View, LoginRequiredMixin):

    template_name = 'create-item.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request: HttpRequest):
        item_form = utils.pop_csrf(request.POST, 'amount')
        item = item_services.get_or_create(**item_form)
        profile = profiles_services.profile_from_request(request)
        services.create_user_item(profile, item, request.POST['amount'])
        return redirect('list_items')


@login_required
def remove_item(request: HttpRequest, pk: int):
    services.delete_user_item(pk, profiles_services.profile_from_request(request))
    return redirect('list_items')


class EditItem(View, LoginRequiredMixin):

    template_name = 'edit-item.html'


    def get(self, request: HttpRequest, pk: int):
        context = {
            'item': services.get_user_item(pk, profiles_services.profile_from_request(request))
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, pk: int):
        services.update_user_item(pk, profiles_services.profile_from_request(request), request.POST['amount'])
        return redirect('list_items')
