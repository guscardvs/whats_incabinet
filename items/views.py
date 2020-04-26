from time import sleep

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from core import models as core_models
from core import utils as core_utils


# Create your views here.
class ListItems(View, LoginRequiredMixin):

    template_name = 'list-items.html'

    def context(self, request: HttpRequest) -> dict:
        return dict(items=core_models.Profile.objects.get(user=request.user).item.all())

    def get(self, request):
        print(self.context(request))
        return render(request, self.template_name, self.context(request))

    def post(self, request):
        form = core_utils.format_form(request.POST)
        profile = core_models.Profile.objects.get(user=request.user)
        if len(profile.item.filter(item=core_models.Item.objects.get(name=form['name']))) != 0:
            context = self.context(request)
            context['error'] = "Item já cadastrado"
            return render(request, self.template_name, context)
        item = core_models.UserItem.create_user_item(
            **core_utils.format_form(form))
        if item is not None:
            item.save()
            profile.item.add(item)
        else:
            context = self.context
            context['error'] = 'Ops, algum erro ocorreu :(, Tente novamente.'
            return render(request, self.template_name, context)
        profile.save()
        return render(request, self.template_name, self.context(request))


class CreateItem(View):

    template_name = 'create-item.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        item_form = core_utils.format_form(request.POST, 'amount')
        item = core_models.Item(**item_form)
        uitem = core_models.UserItem.create_user_item(**request.POST)
        uitem.save()
        profile = core_models.Profile.objects.get(user=request.user)
        profile.item.add(uitem)
        profile.save()
        return redirect('list_items')


@login_required
def remove_item(request, pk: str):
    profile = core_models.Profile.objects.get(user=request.user)
    uitem = core_models.UserItem.objects.get(pk=pk)
    profile.item.remove(uitem)
    profile.save()
    uitem.delete()
    return redirect('list_items')
