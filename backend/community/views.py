from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from stock.models import Stock

# Create your views here.
def post_list(request):
    posts = Post.objects.order_by('-pk')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/post_list.html', context)


def post_create(request):
    if request.user.is_authenticated:
        stocks = Stock.objects.all()
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                return redirect('community:post_list')
        else:
            form = PostForm()

        context = {
            'stocks': stocks,
            'form': form,
            'positions': ['홀드','매수','매도']
        }
        return render(request, 'community/post_form.html', context)
    else:
        return redirect('accounts:login')


def post_detail(request, post_pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=post_pk)
        stock = Stock.objects.all().get(name=post.stock)
        context = {
            'post': post,
            'stock': stock,
        }
        return render(request, 'community/post_detail.html', context)
    else:
        return redirect('accounts:login')   


def post_update(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('community:post_list')
    if request.method =="POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community:post_detail', post_pk)
    else:
        form = PostForm(instance=post)
    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'community/post_form.html', context)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.user != post.user:
        return redirect('community:post_list')
    post.delete()
    return redirect('community:post_list')
