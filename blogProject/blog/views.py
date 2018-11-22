from django.shortcuts import render,get_object_or_404
from .models import post
from taggit.models import Tag
from .form import EmailsendForm,commentForm
from django.core.mail import send_mail
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
# Create your views here.
def post_view(request,tag_slug=None):
    post_list=post.objects.all()
    tag=None
    if (tag_slug):
        tag=get_object_or_404(Tag,slug=tag_slug)
        post_list=post_list.filter(tags__in=[tag])

    paginator=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=paginator.page(page_number)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.page(paginator.num_pages)

    return render(request,'blog/blog.html',{'post_list':post_list,'tag':tag})
def post_detailview(request,year,month,day,Post):
    Post=get_object_or_404(post,slug=Post,status='published',publish__year=year,publish__month=month,publish__day=day)
    comments=Post.comments.filter(active=True)

    csubmit=False
    if request.method=="POST":
        form=commentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.Post=Post
            new_comment.save()
            csubmit=True
    else:
        form=commentForm()
    return render(request,'blog/post_detail.html',{'post':Post,'form':form,'csubmit':csubmit,'comments':comments})
def sharMailView(request,id):
    Post=get_object_or_404(post,id=id,status='published')
    sent=False
    if request.method=="POST":
        form=EmailsendForm(request.POST)
        if form.is_valid():
           cd=form.cleaned_data
           subject='{}({}) recommnded to please read {}'.format(cd['name'],cd['email'],Post.title)
           post_url=request.build_absolute_uri(Post.get_absolute_url())
           message='read post at:\n{}\n{}\n\ncomments:\n\n{}'.format(post_url,cd['name'],cd['comments'])

           send_mail(subject,message,cd['email'],[cd['to']])
           sent=True
    else:
        form=EmailsendForm()
    return render(request,'blog/sharemail.html',{'form':form,'post':Post,'sent':sent})
