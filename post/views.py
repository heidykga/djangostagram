from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView, UpdateView
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from dsuser.decorators import login_required
from django.db import transaction
from django.http import Http404
from django.db.models import Q
from dsuser.models import Dsuser
from tag.models import Tag
from .models import Post
from .forms import PostForm

# Create your views here.

@method_decorator(login_required, name='dispatch')
class PostWriteView(FormView):
    template_name = 'post_write.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        with transaction.atomic():
            post = Post(
                title=form.data.get('title'),
                writer=Dsuser.objects.get(userid=self.request.session.get('user')),
                image=form.data.get('image'),
                contents=form.data.get('contents')
            )

            tags = form.data.get('tags').split(',')

            post.save()

            for tag in tags:
                if not tag:
                    continue

                _tag, _ = Tag.objects.get_or_create(name=tag)
                post.tags.add(_tag)

        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect('/' )

    def get_form_kwargs(self, **kwargs):
        kw = super().get_form_kwargs(**kwargs)
        kw.update({
            'request': self.request
        })
        return kw

class TimeLine(ListView):
    model = Post
    template_name = 'timeline.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        query = self.request.GET.get('s')
        
        if query:
            product_list = self.model.objects.filter( Q(title__icontains=query) | Q(tags__name__icontains=query) ).order_by('-registered_dttm')
        else:
            product_list = self.model.objects.all().order_by('-registered_dttm')
        return product_list

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  
        max_index = len(paginator.page_range)

        try:
            current_page = int(request.GET.get('page', '1'))
        except:
            current_page = 1
       
        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context

class PostDetailView(DetailView):
    template_name = 'post_detail.html'
    queryset = Post.objects.all()
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(self.request)
        return context

    def get_object(self):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post

class PostUpdateView(UpdateView):
    model = Post   
    form_class= PostForm
    template_name = 'post_update.html'
    context_object_name = 'post'
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(self.request)
        return context

    def get_object(self): 
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return post

def delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        post.delete()
    except Post.DoesNotExist:
        raise Http404('게시글을 찾을 수 없습니다')

    return reverse_lazy('/')