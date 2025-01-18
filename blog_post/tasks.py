from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from blog_post.models import PostStatistics, BlogPost, Reaction
from django.utils import timezone

@shared_task
def send_registration_email(user_email):
    """Send Registration email."""

    message = 'Thank you for signing up to Blog!'
    subject = 'Welcome to Blog'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_emails = [user_email]
    send_mail(subject, message, from_email, to_emails)


@shared_task
def generate_daily_post_statistics():
    """Generate Daily stats for all the posts."""
    blogposts = BlogPost.objects.all()
    today = timezone.now().date()

    for post in blogposts:
        
        stats = PostStatistics.objects.filter(post=post, date=today).first()
        if not stats:
            stats = PostStatistics(post=post, date=today)
        stats.likes = post.reactions.filter(reaction=Reaction.ReactionChoices.LIKE, created_at=today).count()
        stats.comments = post.comments.filter(created_at=today).count()
        stats.save()

    return f"Stats generated for {blogposts.count()} posts on {today}."
