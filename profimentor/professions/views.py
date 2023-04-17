from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import *
from .models import *
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import ProfessionsSerializer
from .utils import *

class ProfessionsAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 2
class ProfessionsAPIList(generics.ListCreateAPIView):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = ProfessionsAPIListPagination

class ProfessionsAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer
    permission_classes = (IsAuthenticated, )


class ProfessionsAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Professions.objects.all()
    serializer_class = ProfessionsSerializer
    permission_classes = (IsAdminOrReadOnly, )

# class ProfessionsAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Professions.objects.all()
#     serializer_class = ProfessionsSerializer


# class ProfessionsViewSet(viewsets.ModelViewSet):
#     # queryset = Professions.objects.all()
#     serializer_class = ProfessionsSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get("pk")
#
#         if not pk:
#             return Professions.objects.all()[:]
#
#         return Professions.objects.filter(pk=pk)
#
#
#     @action(methods=['get'], detail=True)
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         return Response({'cats': cats.name})
#










class ProfessionsHome(DataMixin, ListView):
    model = Professions
    template_name = 'professions/index.html'
    context_object_name = 'posts'



    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная Страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Professions.objects.filter().select_related('cat')
# def index(request):
#     posts = Professions.objects.all()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Главная Страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'professions/index.html', context=context)

def about(request):
    return render(request, 'professions/about.html', {'title': 'О Сайте'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'professions/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление Статьи")
        return dict(list(context.items()) + list(c_def.items()))

# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             #print(form.cleaned_data)
#
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'professions/addpage.html', {'form': form, 'menu': menu, 'title': 'Добавление статьи'})

# def contact(request):
#     return HttpResponse("Обратная Связь")

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'professions/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

# def login(request):
#     return HttpResponse("Авторизация")



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DataMixin, DetailView):
    model = Professions
    template_name = 'professions/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))

# def show_post(request, post_slug):
#     post = get_object_or_404(Professions, slug=post_slug)
#
#     context = {
#         'post': post,
#         'menu': menu,
#         'title': post.title,
#         'cat_selected': 1,
#
#     }
#     return render(request, 'professions/post.html', context=context)

class ProfessionsCategory(DataMixin, ListView):
    model = Professions
    template_name = 'professions/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Professions.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# def show_category(request, cat_id):
#     posts = Professions.objects.filter(cat_id=cat_id)
#
#
#     if len(posts) == 0:
#         raise Http404()
#
#     context = {
#         'posts': posts,
#         'menu': menu,
#         'title': 'Отображение по рубрикам',
#         'cat_selected': cat_id,
#     }
#     return render(request, 'professions/index.html', context=context)

class RegisterUser(DataMixin, CreateView):
    form_class = UserCreationForm
    template_name = 'professions/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'professions/login.html'

    def get_context_data(self, *, object_lost=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')