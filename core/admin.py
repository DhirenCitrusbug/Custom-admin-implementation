from django.contrib import admin
from core.models import *


# Register your models here.
class AllFieldAdmin(admin.ModelAdmin):

    def __init__(self, model, admin_site):

        self.list_display = [
            field.name for field in model._meta.fields
        ]

        super(AllFieldAdmin, self).__init__(model, admin_site)


admin.site.register(User, AllFieldAdmin)
admin.site.register(ReviewCategory, AllFieldAdmin)
admin.site.register(ReviewBrand, AllFieldAdmin)
admin.site.register(Review, AllFieldAdmin)
admin.site.register(ReviewGeneral, AllFieldAdmin)
admin.site.register(ReviewFrameset, AllFieldAdmin)
admin.site.register(ReviewDrivetrain, AllFieldAdmin)
admin.site.register(ReviewComponents, AllFieldAdmin)
admin.site.register(ReviewEbikeSystems, AllFieldAdmin)
admin.site.register(ReviewAccessories, AllFieldAdmin)
admin.site.register(ReviewGalley, AllFieldAdmin)
admin.site.register(Pages, AllFieldAdmin)
admin.site.register(Menus, AllFieldAdmin)
admin.site.register(TrustedAccessories, AllFieldAdmin)
admin.site.register(ImageGallery, AllFieldAdmin)
admin.site.register(ReviewHighlights, AllFieldAdmin)
admin.site.register(UpVoteReviewHighlights, AllFieldAdmin)
admin.site.register(Comments, AllFieldAdmin)
admin.site.register(ModelYear, AllFieldAdmin)
admin.site.register(BikeClass, AllFieldAdmin)
admin.site.register(WheelSize, AllFieldAdmin)
admin.site.register(FrameType, AllFieldAdmin)
admin.site.register(BreakType, AllFieldAdmin)
admin.site.register(UpVote, AllFieldAdmin)
admin.site.register(ContactUs, AllFieldAdmin)
admin.site.register(VisitorHistory, AllFieldAdmin)

