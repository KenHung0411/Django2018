from django.shortcuts import render,get_object_or_404,redirect
from django.http import Http404
from .models import Posts, Comment
from datetime import datetime
from .forms import CommentForm

# Create your views here.
def index(request):
	now = datetime.now()
	content = {
    	'date': now.strftime('%Y-%m-%d')
	}

	return render(request,'blog/index.html',content)


def post_list(request):
	now = datetime.now()
	try:
		posts = Posts.objects.all()
		content = {'posts':posts,
				   'date': now.strftime('%Y-%m-%d')
		}
	except Posts.DoesNotExist:
		raise Http404("Post Does Not exist")

	return render(request,'blog/post_list.html',content)


def post_detail(request, pk):
	now = datetime.now()
	post = get_object_or_404(Posts, pk=pk)
	c_number = len(Comment.objects.filter(post_id = pk))
	content = {
		'date': now.strftime('%Y-%m-%d'),
		'post':post,
		'c_number':c_number
	}

	return render(request, 'blog/post_detail.html',content)


def post_comment(request, pk):
	comments = Comment.objects.filter(post_id = pk)
	comments_count = len(comments)
	p_id = pk
	content = {
		'comments' : comments,
		'comments_count': comments_count,
		'p_id': p_id 
	}
	return render(request, 'blog/comment_detail.html', content)


def add_comment(request,pk):
	if request.method == 'POST':
		form = CommentForm(request.Post)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.name = request.Post['name']
			comment.comment = request.Post['comment']
			comment.post_id = pk
			comment.save()
			return redirect('post_detail', pk=pk)
		else:
			pass
	else:
		form = CommentForm()
		return render(request, 'blog/add_comment.html', {'form':form})