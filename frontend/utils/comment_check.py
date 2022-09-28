import akismet
from django.conf import settings


def comment_check(user_ip, user_agent, comment_author, comment_author_email, comment_content):
    akismet_api = akismet.Akismet(key=settings.PYTHON_AKISMET_API_KEY, blog_url=settings.PYTHON_AKISMET_BLOG_URL)
    check_spam = akismet_api.comment_check(
        user_ip=user_ip, user_agent=user_agent, comment_author=comment_author,
        comment_author_email=comment_author_email, comment_content=comment_content
    )
    return check_spam
