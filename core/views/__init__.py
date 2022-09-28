from .users import (
    IndexView,
    # UserListView,
    # UserDetailsView,
    # UserDeleteView,
    # UserCreateView,
    UserUpdateView,
    UserPasswordView,
    # UserAjaxPagination,
)
from .review_category import (
    ReviewCategoryListView, ReviewCategoryDetailView, ReviewCategoryCreateView, ReviewCategoryUpdateView, ReviewCategoryDeleteView,
    ReviewCategoryAjaxPagination
)
from .review_brand import (
    ReviewBrandListView, ReviewBrandCreateView, ReviewBrandUpdateView, ReviewBrandDeleteView,
    ReviewBrandAjaxPagination
)
from .review import (
    ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView, ReviewAjaxPagination, upload_image_gallery,
    get_image_gallery, gallery_image_details, gallery_image_delete, gallery_image_edit, review_slug_check
)
from .pages import (
    PagesListView, PagesCreateView, PagesUpdateView, PagesDeleteView, PagesAjaxPagination
)
from .menus import (
    MenusListView, MenusCreateView, MenusUpdateView, MenusDeleteView, MenusAjaxPagination
)
from .trusted_accessories import (
    TrustedAccessoriesListView, TrustedAccessoriesCreateView, TrustedAccessoriesUpdateView,
    TrustedAccessoriesDeleteView, TrustedAccessoriesAjaxPagination
)
from .comments import (
    CommentsListView, CommentsCreateView, CommentsUpdateView,
    CommentsDeleteView, CommentsAjaxPagination, approve_disapprove_comment, spam_unspam_comment, empty_spam_comment, unsubscribe_comment
)
