from django_components import register, Component, EmptyTuple, EmptyDict
from django_tables2 import tables, LinkColumn, A
from blog.models import Post
from pprint import pprint


class PostsTable(tables.Table):
    title = LinkColumn('post_detail', args=[A('id')], verbose_name='Title')
    content = LinkColumn('post_detail', args=[A('id')], verbose_name='Content')
    author = LinkColumn('author_detail', args=[A('id')], verbose_name='Author')

    class Meta:
        model = Post
        template_name="posts_table/custom_template.html"
        fields = (
            'title',
            'content',
            'published_date',
            'author',
            'created_at'
        )

@register("posts-table")
class PostsTableComponent(Component):
    template_name = 'posts_table/template.html'

    class Media:
        css = 'posts_table/style.css'
        js = 'posts_table/script.js'

    def __init__(self, *args, **kwargs):
        self.outer_context = kwargs.get('outer_context')

        if self.outer_context:
            self.request = kwargs.get('outer_context').get('request')
            self.queryset = kwargs.get('outer_context').get('queryset')

        super().__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)

        if self.outer_context:
            context['table'] = PostsTable(
                    data=self.queryset,
                    order_by=self.request.GET.get("sort", "created_at")
                ) \
                .paginate(
                    page=self.request.GET.get("page", 1),
                    per_page=10
                )

        return context



