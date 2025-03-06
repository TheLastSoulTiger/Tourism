from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Tour, Tag, HeaderCarouselImage
from .forms import PostForm
from .forms import ReviewForm
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator


def search_post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/post_detail.html', {'post': post})


def home(request):
    posts = Post.objects.order_by('-created_date')[:3]
    tag_id = request.GET.get('tag')
    tours = Tour.objects.filter(tags__id=tag_id) if tag_id else Tour.objects.all()
    tags = Tag.objects.all()
    header_carousel_images = HeaderCarouselImage.objects.all()

    context = {
        'posts': posts,
        'tours': tours,
        'tags': tags,
        'header_carousel_images': header_carousel_images,
    }
    return render(request, 'blog/home.html', context)

   
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})


def about(request):
    return render(request, 'blog/about.html')


def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    else:
        posts = Post.objects.all()

    paginator = Paginator(posts, 5)  # 5 postów na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def add_review(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.tour = tour
            review.save()
            return redirect('tour_detail', id=tour.id)
    else:
        form = ReviewForm()
    return render(request, 'blog/add_review.html', {'form': form, 'tour': tour})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(
                    f'Контакт от {name}',
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                return render(request, 'blog/contact_success.html', {'name': name})
            except BadHeaderError:
                return render(request, 'blog/contact_error.html', {'error': 'Invalid header found.'})
    else:
        form = ContactForm()
    return render(request, 'blog/contact.html', {'form': form})


def tour_detail(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    reviews = tour.reviews.all()
    paginator = Paginator(reviews, 5)  # 5 recenzji na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'tour_detail.html', {'tour': tour, 'page_obj': page_obj})
