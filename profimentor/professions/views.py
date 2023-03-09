from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from .forms import *
from .models import *

menu = [{'title':"О сайте", 'url_name':'about'},
        {'title':"Добавить статью", 'url_name':'add_page'},
        {'title':"Обратная связь", 'url_name':'contact'},
        {'title':"Войти", 'url_name':'login'}
]

class ProfessionsHome(ListView):
    model = Professions
    template_name = 'professions/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = menu
        context['title'] = 'Главная Страница'
        context['cat_selected'] = 0
        return context

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

class AddPage(CreateView):
    form_class = AddPostForm
    template_name = 'professions/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи'
        context['menu'] = menu
        return context

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

def contact(request):
    return HttpResponse("Обратная Связь")

def login(request):
    return HttpResponse("Авторизация")



def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

class ShowPost(DetailView):
    model = Professions
    template_name = 'professions/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self,*, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post']
        context['menu'] = menu
        return context

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

class ProfessionsCategory(ListView):
    model = Professions
    template_name = 'professions/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Professions.objects.filter(cat__slug=self.kwargs['cat_slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context =super().get_context_data(**kwargs)
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['menu'] = menu
        context['cat_selected'] = context['posts'][0].cat_id
        return context

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
