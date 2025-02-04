from catalogs.models import Catalog
from django.shortcuts import redirect, get_object_or_404, render
from django.utils import timezone
from .models import Post, Comment
from tags.models import Tag
from datetime import datetime



def post_list(request):

    categories = request.GET.getlist('category')
    hashtags = request.GET.getlist('hashtag')
    sort_by = request.GET.get('sort', 'latest')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    all_categories = Catalog.objects.all()
    all_tags = Tag.objects.all()


    queryset = Post.objects.all()


    if categories:
        queryset = queryset.filter(category__name__in=categories)


    if hashtags:
        queryset = queryset.filter(tags__title__in=hashtags)


    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        queryset = queryset.filter(publish__range=[start_date, end_date])

    elif start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        queryset = queryset.filter(publish__gte=start_date)

    elif end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
        queryset = queryset.filter(publish__lte=end_date)

    if sort_by == 'popular':
        queryset = queryset.order_by('-views')  #
    elif sort_by == 'oldest':
        queryset = queryset.order_by('publish')
    elif sort_by == 'latest':
        queryset = queryset.order_by('-publish')
    else:
        queryset = queryset.order_by('-publish')


    posts = queryset

    ctx = {'posts': posts,
           'categories': categories,
           'hashtags': hashtags,
           'sort_by': sort_by,
           'start_date': start_date,
           'end_date': end_date,
           'all_categories': all_categories,
           'all_tags': all_tags,
           }


    return render(request, 'index_with_side_bar.html',ctx )


def post_detail(request, year, month, day, slug):
    post = get_object_or_404(
        Post,
        slug=slug,
        created_at__year=year,
        created_at__month=month,
        created_at__day=day,
    )

    post.views += 1
    post.save(update_fields=['views'])

    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        content = request.POST.get('content')
        publish = request.POST.get('publish')

        if not publish:
            publish = timezone.now()

        comment = Comment(
            post=post,
            name=name,
            email=email,
            content=content,
            publish=publish
        )
        comment.save()

        return redirect('posts:detail', year=post.created_at.year, month=post.created_at.month,
                        day=post.created_at.day, slug=post.slug)

    ctx = {
        'post': post,
        'comments': comments,
    }

    return render(request, 'posts/post-detail.html', ctx)

