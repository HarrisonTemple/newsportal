from news.models import *
admin = User.objects.create_user(username="admin", password="abc123")
guest = User.objects.create_user(username="guest", password="bcd321")

admin_author = Author.objects.create(user_id = admin)
guest_author = Author.objects.create(user_id = guest)

cat1 = Category.objects.create(cat_name = "politics")
cat2 = Category.objects.create(cat_name = "economy")
cat3 = Category.objects.create(cat_name = "history")
cat4 = Category.objects.create(cat_name = "society")

post_ar_1 = Post.objects.create(post_type = "ar", author= admin_author, title = "modern politics", content ="modern politics is cool")
post_ar_1.category.set([cat1, cat4])

post_ar_2 = Post.objects.create(post_type = "ar", author= guest_author, title = "history today", content ="we make the history today ")
post_ar_2.category.set([cat3, cat4])

post_nw_1 = Post.objects.create(post_type = "nw", author = admin_author, title = "breaking news", content = "you won't believe what just happened today")
post_nw_1.category.set([cat4, cat3])

comm1 = Comment.objects.create(post_id = post_ar_1, user_id = guest, content = "so cool")
comm2 = Comment.objects.create(post_id = post_ar_2, user_id = admin, content = "this article hits hard frfr")
comm3 = Comment.objects.create(post_id = post_ar_1, user_id = guest, content = "so cool")
comm4 = Comment.objects.create(post_id = post_nw_1, user_id = admin, content = "there is no way this happened")
comm5 = Comment.objects.create(post_id = post_nw_1, user_id = guest, content = "another clickbait :docnotL:")
comm6 = Comment.objects.create(post_id = post_ar_2, user_id = guest, content = "holy smokes i learned so much while writing this article")
comm7 = Comment.objects.create(post_id = post_ar_1, user_id = admin, content = "so cool")

post_ar_2.like()
post_ar_1.like()
post_ar_1.like()
post_nw_1.like()
post_ar_2.dislike()
post_nw_1.like()
post_ar_2.like()
post_ar_1.like()
comm1.dislike()
comm2.dislike()
comm1.like()
comm4.dislike()
comm1.like()
comm7.like()
comm1.dislike()
comm2.like()
comm1.dislike()
comm5.like()

admin_author.update_rating()
guest_author.update_rating()

Author.objects.all().order_by("-rating").values("user_id__username")[0]

best_post = Post.objects.all().order_by("-rating")[0]
best_post.author.user_id.username
best_post.rating
best_post.title
best_post.preview()

Comment.objects.filter(post_id = best_post).values("user_id__username", "publish_date", "content", "rating")

