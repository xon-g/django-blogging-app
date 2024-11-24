from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import date
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView

from .models import Post, Comment, Author
from .forms import CommentForm

# from pprint import pprint

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['queryset'] = self.object_list
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

    def get_comments(self, per_page=10):
        paginator = Paginator(self.object.comment_set.all().order_by('-created_at'), per_page)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return page_obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_comments()
        context['form'] = CommentForm()
        context['offset'] = context['comments'].paginator.per_page * (context['comments'].number - 1)
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author_id = request.user.author.id
            comment.post = self.get_object()
            comment.save()
            return redirect('post_detail', pk=self.kwargs['pk'])
        else:
            return render(request, self.template_name, self.get_context_data())

class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)

class LoadMoreCommentsView(View):
    def get(self, request, *args, **kwargs):
        post_id = kwargs['pk']
        post = Post.objects.get(id=post_id)
        offset = int(request.GET.get('offset', 0))
        per_page = 10
        comments = post.comment_set.all().order_by('-created_at')[offset:offset+per_page]

        comments_html = ''
        for comment in comments:
            comments_html += f'''
                <div class="comment">
                    <a href="{reverse('author_detail', args=[comment.author.id])}" class="text-sm font-bold text-[#4b7dc4]">{comment.author}</a>
                    <p class="text-xs italic">{ date(comment.created_at, "M. j, Y, g:i A") }</p>
                    <p class="text-sm mt-1">{ comment.body }</p>
                    <hr class="my-4 opacity-25">
                </div>
            '''

        # Add a load more button if there are more comments
        if post.comment_set.count() > offset+per_page:
            comments_html += f'''
                <button
                    class="load-more-comments bg-[#4b7dc4] text-white py-2 px-4 rounded mt-5"
                    hx-get="{reverse('post_load_more_comments', args=[post_id])}?offset={offset+per_page}"
                    hx-target=".load-more-comments"
                    hx-swap="beforebegin"
                >
                    Load More Comments
                </button>
            '''
        else:
            comments_html += f'''
                <p class="text-sm">No more comments</p>
            '''

        return HttpResponse(comments_html)

class AuthorListView(ListView):
    model = Author
    template_name = 'author_list.html'
    context_object_name = 'authors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        context['queryset'] = self.object_list
        return context

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.post_set.all()
        return context