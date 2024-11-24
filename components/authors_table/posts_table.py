from django_components import register, Component, EmptyTuple, EmptyDict
from django_tables2 import tables, LinkColumn, A
from blog.models import Author
from pprint import pprint


class AuthorsTable(tables.Table):
    name = LinkColumn('author_detail', args=[A('id')], verbose_name='Name')
    email = LinkColumn('author_detail', args=[A('id')], verbose_name='Email')

    class Meta:
        model = Author
        template_name="authors_table/custom_template.html"
        fields = (
            'name',
            'email',
        )

@register("authors-table")
class PostsTableComponent(Component):
    template_name = 'authors_table/template.html'

    class Media:
        css = 'authors_table/style.css'
        js = 'authors_table/script.js'

    def __init__(self, *args, **kwargs):
        self.outer_context = kwargs.get('outer_context')

        if self.outer_context:
            self.request = kwargs.get('outer_context').get('request')
            self.queryset = kwargs.get('outer_context').get('queryset')

        super().__init__(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data( *args, **kwargs)

        if self.outer_context:
            context['table'] = AuthorsTable(
                    data=self.queryset,
                    order_by=self.request.GET.get("sort", "created_at")
                ) \
                .paginate(
                    page=self.request.GET.get("page", 1),
                    per_page=10
                )

        return context



