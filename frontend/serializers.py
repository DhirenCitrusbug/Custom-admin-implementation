from django.db.models import Q, Count
from rest_framework import serializers
from core.models import Comments
from datetime import datetime

class CommentSerializer(serializers.ModelSerializer):
    replied_comments = serializers.SerializerMethodField('child_comments')
    upvote_count = serializers.SerializerMethodField('comment_upvote_count')
    create_at = serializers.SerializerMethodField('create_at_date')
    
    class Meta:
        model = Comments
        fields =  ['id', 'name', 'email', 'description', 'parent_id', 'upvote_count', 'replied_comments', 'create_at']
        
    def child_comments(request, obj):
        child_comment = Comments.objects.filter(comment_type='Review', parent_id=obj.id, is_approved=True).annotate(upvote_count = Count('upvote__comment_id')).order_by('-upvote_count')
        replied_comments = []
        for comment in child_comment:
            serializers = CommentSerializer(comment)
            replied_comments.append(serializers.data)
        return replied_comments
    
    def comment_upvote_count(request, obj):
        return obj.upvote_count
    
    def create_at_date(request, obj):
        today_time = datetime.now()
        if obj.create_at.day == today_time.day:
            return str(today_time.hour - obj.create_at.hour) + " Hours ago"
        else:
            if obj.create_at.month == today_time.month:
                return str(today_time.day - obj.create_at.day) + " Days ago"
            else:
                if obj.create_at.year == today_time.year:
                    return str(today_time.month - obj.create_at.month) + " Months ago"
                else:
                    return str(today_time.year - obj.create_at.year) + " Years ago"
        return obj.create_at