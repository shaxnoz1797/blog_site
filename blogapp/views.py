
from django.shortcuts import get_object_or_404, render
from django.template.defaulttags import comment
from django.utils.translation.trans_null import activate
from .forms import CommentForm  # Yangi yaratgan formamizni chaqiramiz
from .models import Post
from django.views.generic import ListView


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = "blog/post/list.html"




def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,
                             status="published",
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Faqat tasdiqlangan (active=True) izohlarni olamiz
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # Foydalanuvchi izoh yozib "Yuborish"ni bossa
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Ma'lumotni vaqtincha ushlab turamiz (bazaga yozmaymiz)
            new_comment = comment_form.save(commit=False)
            # Izohni aynan shu postga bog'laymiz
            new_comment.post = post
            # Endi bazaga saqlaymiz
            new_comment.save()
    else:
        # Sahifaga shunchaki kirganda bo'sh forma ko'rinadi
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })




def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Yo'l: templates papkasidan keyingi qism yoziladi
    return render(request, 'blog/post/share.html', {'post': post})

