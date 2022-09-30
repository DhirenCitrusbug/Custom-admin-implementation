from django.core.mail import send_mail


def send_reply_mail(comment, unsubscribe_url):
    message = 'Any one user reply on your comment.{}'.format(unsubscribe_url)
    result = send_mail('Reply on your comment.', message, 'vicky@electricbikereview.com', [comment.parent_id.email])
    print("helloooo")
    print(result)
    return True


# def send_reply_mail(comment, url):
#     message = 'Any one user reply on your comment. \n link:- <a href="{}" >{}<a>'.format(url, url)
#     result = send_mail('Reply on your comment.', message, 'vicky@electricbikereview.com', [comment.parent_id.email])
#     print("helloooo")
#     print(result)
#     return True
