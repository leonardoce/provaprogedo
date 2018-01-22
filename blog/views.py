from django import forms
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponse
from blog.models import Post, Category, Comment
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget


def ciao(request):
    return HttpResponse("ciao")


def index(request):
    object_list = Post.objects.filter(is_published=True)
    category_list = Category.objects.all()
    return render(request, "blog/index.html", {
        'object_list': object_list,
        'category_list': category_list})


def category(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    object_list = Post.objects.filter(category=cat, is_published=True)
    category_list = Category.objects.all()
    return render(request, "blog/category.html", {
        'category': cat,
        'object_list': object_list,
        'category_list': category_list})


class CommentForm(forms.Form): # from django import forms
    author = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)
    captcha = ReCaptchaField(widget=ReCaptchaWidget())


class PostView(FormView):
    form_class = CommentForm
    template_name = 'blog/post.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)

        p = get_object_or_404(Post, slug=self.kwargs['slug'])
        category_list = Category.objects.all()

        context['post'] = p
        context['category_list'] = category_list

        return context

    def form_valid(self, form):
        email = form.cleaned_data['author']
        content = form.cleaned_data['content']

        c = Comment()
        c.content = content
        c.date = timezone.now()
        c.post = get_object_or_404(Post, slug=self.kwargs['slug'])
        try:
            c.author = User.objects.get(email=email)
        except User.DoesNotExist:
            c.author = User.objects.create_user(username=email, email=email)
            c.author.save()

        c.save()

        return super(PostView, self).form_valid(form)

    def get_success_url(self):
        p = get_object_or_404(Post, slug=self.kwargs['slug'])
        return p.get_absolute_url()
