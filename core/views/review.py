# -*- coding: utf-8 -*-
"""
This is a view module to define list, create, update, delete views.

You can define different view properties here.
"""
import datetime

from django.db.models import Q
from django.template.loader import get_template
from django_datatables_too.mixins import DataTableMixin
from django.shortcuts import reverse, redirect

from core.mixins import HasPermissionsMixin
from core.views.generic import (
    MyListView, MyDetailView, MyCreateView, MyUpdateView, MyDeleteView, MyLoginRequiredView, MyNewFormsetCreateView
)
from core.forms import ReviewCreationForm, ReviewChangeForm
from core.models import (
    Review, ReviewGalley, ReviewGeneral, ReviewFrameset, ReviewDrivetrain, ReviewComponents, ReviewEbikeSystems,
    ReviewAccessories,  ReviewCategory, ReviewBrand, ImageGallery, ReviewHighlights, ModelYear, BikeClass, 
    FrameType, WheelSize, BreakType
)

from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import get_image_dimensions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.utils import review_view_slugify


# -----------------------------------------------------------------------------
# Review Views
# -----------------------------------------------------------------------------
# class ReviewSpecificationInline(InlineFormSetFactory):
#     model = ReviewSpecification
#     form_class = ReviewSpecificationCreationForm
#     factory_kwargs = {'extra': 1, 'can_delete': False}


class ReviewListView(MyListView):
    """
    View for Review listing
    """
    # paginate_by = 25
    ordering = ["-id"]
    model = Review
    queryset = model.objects.all()
    template_name = "core/review/review_list.html"
    permission_required = ("core.view_review",)


class ReviewCreateView(MyCreateView):
    """
    View to create Review
    """
    model = Review
    form_class = ReviewCreationForm
    template_name = "core/review/review_form.html"
    permission_required = ("core.add_review",)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super(ReviewCreateView, self).get_context_data()
        review_brand = ReviewBrand.objects.all().order_by('-id')
        review_category = ReviewCategory.objects.all().order_by('-id')
        context['review_brand'] = review_brand
        context['review_category'] = review_category
        context['review_model_year'] = ModelYear.objects.all().order_by('id')
        context['review_bike_class'] = BikeClass.objects.all().order_by('id')
        context['review_frame_type'] = FrameType.objects.all().order_by('id')
        context['review_wheel_size'] = WheelSize.objects.all().order_by('id')
        context['review_break_type'] = BreakType.objects.all().order_by('id')
        return context

    def post(self, request, *args, **kwargs):
        """Override POST method"""
        data = request.POST.copy()
        if data['slug']:
            slug = review_view_slugify(Review, None, data['slug'])
        else:
            slug = data['slug']

        qry_review_add = Review(
            name=data['name'], slug=slug, description=data['description'], more_details=data['more_details'],
            meta_title=data['meta_title'], status=data['status'], publish_date=data['publish_date'],
            youtube_video=data['youtube_video'], create_by=request.user,
            featured_image=request.FILES.get('featured_image', None), model_name=data['model_name'],
            model_year=data['model_year'], trim=data['trim']
        )
        qry_review_add.save()
        for model_year_id in data.get('model_year').split(','):
            model_year_obj = ModelYear.objects.get_or_create(year=model_year_id)[0]
            qry_review_add.demo_model_year.add(model_year_obj.id)
        for categories_id in data.getlist('categories'):
            qry_review_add.categories.add(categories_id)
        for brand_id in data.getlist('brands'):
            qry_review_add.brands.add(brand_id)
        # qry_review_add.save()

        highlights = data.getlist('highlight')
        for highlight in highlights:
            if highlight:
                qry_review_highlight = ReviewHighlights(highlight=highlight, review=qry_review_add)
                qry_review_highlight.save()

        if data['gears'] == "":
            data['gears'] = None
        if data['motor_nominal_output'] == "":
            data['motor_nominal_output'] = None
        if data['battery_watt_hours'] == "":
            data['battery_watt_hours'] = None
        if data['weight'] == "":
            data['weight'] = None
            
        add_bike_class = []
        add_frame_type = []
        add_wheel_size = []
        add_brake_type = []
        for bike_class_id in data.getlist('bike_class'):
            qry_bike_class = BikeClass.objects.get(id=bike_class_id)
            add_bike_class.append(str(qry_bike_class))
        for frame_type_id in data.getlist('frame_type'):
            qry_frame_type = FrameType.objects.get(id=frame_type_id)
            add_frame_type.append(str(qry_frame_type))
        for wheel_size_id in data.getlist('wheel_size'):
            qry_wheel_size = WheelSize.objects.get(id=wheel_size_id) 
            add_wheel_size.append(str(qry_wheel_size))
        for brake_type_id in data.getlist('brake_type'):
            qry_brake_type = BreakType.objects.get(id=brake_type_id)
            add_brake_type.append(str(qry_brake_type))
            
        qry_review_general_add = ReviewGeneral(
            msrp=data['msrp'], bike_class=add_bike_class, suspension=data['suspension'], frame_type=add_frame_type, gears=data['gears'],
            demo_gear=data['gears'], motor_type=data['motor_type'],  wheel_size= add_wheel_size, brake_type=add_brake_type,
            motor_nominal_output=data['motor_nominal_output'],demo_motor_nominal_output=data['motor_nominal_output'] , battery_watt_hours=data['battery_watt_hours'],
            demo_battery_watt_hours=data['battery_watt_hours'], demo_weight=data['weight'],
            weight=data['weight'], review=qry_review_add
        )
        qry_review_general_add.save()
        for bike_class_id in data.getlist('bike_class'):
            qry_review_general_add.demo_bike_class.add(bike_class_id)
        for frame_type_id in data.getlist('frame_type'):
            qry_review_general_add.demo_frame_type.add(frame_type_id)
        for wheel_size_id in data.getlist('wheel_size'):
            qry_review_general_add.demo_wheel_size.add(wheel_size_id)
        for brake_type_id in data.getlist('brake_type'):
            qry_review_general_add.demo_brake_type.add(brake_type_id)
        # qry_review_general_add.save()
        
        if data['frameset_weight'] == "":
            data['frameset_weight'] = None
        if data['suspension_travel'] == "":
            data['suspension_travel'] = None

        qry_review_frameset_add = ReviewFrameset(
            frameset_frame_type=add_frame_type, demo_frameset_weight=data['frameset_weight'], frameset_weight=data['frameset_weight'], load_capacity=data['load_capacity'], 
            frameset_suspension=data['frameset_suspension'], demo_suspension_travel=data['suspension_travel'],
            suspension_travel=data['suspension_travel'], fork=data['fork'], frameset_wheel_size = add_wheel_size,
            rear_shock=data['rear_shock'], front_wheel=data['front_wheel'], rear_wheel=data['rear_wheel'], front_hub=data['front_hub'],
            rear_hub=data['rear_hub'], tires=data['tires'], review=qry_review_add
        )
        qry_review_frameset_add.save()
        for frameset_frame_type_id in data.getlist('frame_type'):
            qry_review_frameset_add.demo_frameset_frame_type.add(frameset_frame_type_id)
        for frameset_wheel_size_id in data.getlist('wheel_size'):
            qry_review_frameset_add.demo_frameset_wheel_size.add(frameset_wheel_size_id)
            
        if data['drivetrain_gears'] == "":
            data['drivetrain_gears'] = None

        qry_review_drivetrain_add = ReviewDrivetrain(
            drivetrain_gears=data['drivetrain_gears'], demo_drivetrain_gears=data['drivetrain_gears'], shift_levers=data['shift_levers'],
            front_derailleur=data['front_derailleur'], crankset=data['crankset'],
            rear_derailleur=data['rear_derailleur'], electronic_shifting=data['electronic_shifting'],
            internally_geared_hub=data['internally_geared_hub'],
            continually_variable_transmission=data['continually_variable_transmission'], cassette=data['cassette'],
            chainring=data['chainring'], belt_drive=data['belt_drive'], review=qry_review_add
        )
        qry_review_drivetrain_add.save()

        if data['seatpost_diameter'] == "":
            data['seatpost_diameter'] = None

        qry_review_components_add = ReviewComponents(
            headset=data['headset'], stem=data['stem'], handlebar=data['handlebar'], grips=data['grips'],
            seatpost=data['seatpost'], seatpost_diameter=data['seatpost_diameter'], demo_seatpost_diameter=data['seatpost_diameter'], saddle=data['saddle'],
            pedals=data['pedals'], components_brake_type=add_brake_type,front_brake=data['front_brake'], rear_brake=data['rear_brake'], review=qry_review_add
        )
        qry_review_components_add.save()
        for components_brake_type_id in data.getlist('brake_type'):
            qry_review_components_add.demo_components_brake_type.add(components_brake_type_id)

        if data['systems_motor_nominal_output'] == "":
            data['systems_motor_nominal_output'] = None
        if data['systems_battery_watt_hours'] == "":
            data['systems_battery_watt_hours'] = None

        qry_review_ebike_systems_add = ReviewEbikeSystems(
            systems_bike_class=add_bike_class, systems_motor_type=data['systems_motor_type'], motor=data['motor'], additional_motors=data['additional_motors'],
            systems_motor_nominal_output=data['systems_motor_nominal_output'], demo_systems_motor_nominal_output=data['systems_motor_nominal_output'], display=data['display'],
            smart_bike=data['smart_bike'], theft_gps=data['theft_gps'], demo_systems_battery_watt_hours=data['systems_battery_watt_hours'],
            systems_battery_watt_hours=data['systems_battery_watt_hours'], battery=data['battery'], additional_battery=data['additional_battery'],
            charger=data['charger'], review=qry_review_add
        )
        qry_review_ebike_systems_add.save()
        for systems_bike_class_id in data.getlist('bike_class'):
            qry_review_ebike_systems_add.demo_systems_bike_class.add(systems_bike_class_id)

        qry_review_accessories_add = ReviewAccessories(
            lights=data['lights'], fenders=data['fenders'],
            front_rack=data['front_rack'], rear_rack=data['rear_rack'], review=qry_review_add
        )
        qry_review_accessories_add.save()
        if data['image_list'] != '':
            imageArray = eval(data['image_list'])

            for image in imageArray:
                if image:
                    qry_gallery_image = ImageGallery.objects.filter(id=image['image'])
                    if qry_gallery_image.exists():
                        qry_review_galley_add = ReviewGalley(image=qry_gallery_image.first(), review=qry_review_add, order=image['index'])
                        qry_review_galley_add.save()

        return redirect(reverse("core:review-list"))


class ReviewUpdateView(MyUpdateView):
    """
    View to update Review
    """

    model = Review
    form_class = ReviewChangeForm
    template_name = "core/review/review_update_form.html"
    permission_required = ("core.change_review",)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super(ReviewUpdateView, self).get_context_data()
        review_brand = ReviewBrand.objects.all().order_by('-id')
        review_category = ReviewCategory.objects.all().order_by('-id')
        # qyer_review = Review.objects.get(id=id)
        context['review'] = self.get_object()

        context['review_general'] = ReviewGeneral.objects.get(review=self.get_object())
        context['review_frameset'] = ReviewFrameset.objects.get(review=self.get_object())
        context['review_drivetrain'] = ReviewDrivetrain.objects.get(review=self.get_object())
        context['review_components'] = ReviewComponents.objects.get(review=self.get_object())
        context['review_ebike_systems'] = ReviewEbikeSystems.objects.get(review=self.get_object())
        context['review_accessory'] = ReviewAccessories.objects.get(review=self.get_object())
        context['review_highlights'] = ReviewHighlights.objects.filter(review=self.get_object())

        context['review_model_year'] = ModelYear.objects.all().order_by('id')
        context['review_bike_class'] = BikeClass.objects.all().order_by('id')
        context['review_frame_type'] = FrameType.objects.all().order_by('id')
        context['review_wheel_size'] = WheelSize.objects.all().order_by('id')
        context['review_break_type'] = BreakType.objects.all().order_by('id')

        context['review_gallery'] = ReviewGalley.objects.filter(review=self.get_object()).order_by('order')
        context['review_brand'] = review_brand
        context['review_category'] = review_category
        return context

    def post(self, request, pk, *args, **kwargs):
        print("====================================")
        data = request.POST.copy()
        featured_image = request.FILES.get('featured_image', None)
        if data['slug']:
            slug = review_view_slugify(Review, pk, data['slug'])
        else:
            slug = data['slug']
        Review.objects.filter(id=pk).update(
            name=data['name'], description=data['description'], more_details=data['more_details'],
            meta_title=data['meta_title'], status=data['status'], publish_date=data['publish_date'],
            youtube_video=data['youtube_video'], create_by=request.user,
            model_name=data['model_name'], model_year=data['model_year'], trim=data['trim'], slug=slug
        )
        qry_review_update = Review.objects.get(id=pk)
        qry_review_update.slug = data['slug']
        if featured_image is not None:
            qry_review_update.featured_image = featured_image
        qry_review_update.save()

        qry_review_update.categories.clear()
        for categories_id in data.getlist('categories'):
            qry_review_update.categories.add(categories_id)

        qry_review_update.brands.clear()
        for brand_id in data.getlist('brands'):
            qry_review_update.brands.add(brand_id)

        qry_review_update.demo_model_year.clear()
        for model_year_id in data['model_year'].split(','):
            model_year_obj = ModelYear.objects.get_or_create(year=model_year_id)[0]
            qry_review_update.demo_model_year.add(model_year_obj.id)

        qry_review_update.save()
        ReviewHighlights.objects.filter(review=qry_review_update.id).delete()
        highlights = data.getlist('highlight')
        for highlight in highlights:
            if highlight:
                qry_review_highlight = ReviewHighlights(highlight=highlight, review=qry_review_update)
                qry_review_highlight.save()
                
        if data['gears'] == "":
            data['gears'] = None
        if data['motor_nominal_output'] == "":
            data['motor_nominal_output'] = None
        if data['battery_watt_hours'] == "":
            data['battery_watt_hours'] = None
        if data['weight'] == "":
            data['weight'] = None

        add_bike_class = []
        add_frame_type = []
        add_wheel_size = []
        add_brake_type = []
        for bike_class_id in data.getlist('bike_class'):
            qry_bike_class = BikeClass.objects.get(id=bike_class_id)
            add_bike_class.append(str(qry_bike_class))
        for frame_type_id in data.getlist('frame_type'):
            qry_frame_type = FrameType.objects.get(id=frame_type_id)
            add_frame_type.append(str(qry_frame_type))
        for wheel_size_id in data.getlist('wheel_size'):
            qry_wheel_size = WheelSize.objects.get(id=wheel_size_id)
            add_wheel_size.append(str(qry_wheel_size))
        for brake_type_id in data.getlist('brake_type'):
            qry_brake_type = BreakType.objects.get(id=brake_type_id)
            add_brake_type.append(str(qry_brake_type))

        ReviewGeneral.objects.filter(review=pk).update(
            msrp=data['msrp'], bike_class=add_bike_class, frame_type=add_frame_type, wheel_size=add_wheel_size,
            brake_type=add_brake_type, suspension=data['suspension'], gears=data['gears'], demo_gear=data['gears'],
            motor_type=data['motor_type'], motor_nominal_output=data['motor_nominal_output'], demo_motor_nominal_output=data['motor_nominal_output'],
            battery_watt_hours=data['battery_watt_hours'], demo_battery_watt_hours=data['battery_watt_hours'], weight=data['weight'], demo_weight=data['weight']
        )
        qry_review_general_update = ReviewGeneral.objects.get(review=pk)
        qry_review_general_update.demo_bike_class.clear()
        for bike_class_id in data.getlist('bike_class'):
            qry_review_general_update.demo_bike_class.add(bike_class_id)

        qry_review_general_update.demo_frame_type.clear()
        for frame_type_id in data.getlist('frame_type'):
            qry_review_general_update.demo_frame_type.add(frame_type_id)

        qry_review_general_update.demo_wheel_size.clear()
        for wheel_size_id in data.getlist('wheel_size'):
            qry_review_general_update.demo_wheel_size.add(wheel_size_id)

        qry_review_general_update.demo_brake_type.clear()
        for brake_type_id in data.getlist('brake_type'):
            qry_review_general_update.demo_brake_type.add(brake_type_id)
        qry_review_general_update.save()


        if data['frameset_weight'] == "" or data['frameset_weight'] == 'None':
            data['frameset_weight'] = None
        if data['suspension_travel'] == "":
            data['suspension_travel'] = None

        ReviewFrameset.objects.filter(review=pk).update(
            frameset_frame_type=add_frame_type, frameset_weight=data['frameset_weight'],
            demo_frameset_weight=data['frameset_weight'], load_capacity=data['load_capacity'],
            frameset_suspension=data['frameset_suspension'], demo_suspension_travel=data['suspension_travel'],
            suspension_travel=data['suspension_travel'], fork=data['fork'], rear_shock=data['rear_shock'],
            frameset_wheel_size=add_wheel_size, front_wheel=data['front_wheel'], rear_wheel=data['rear_wheel'],
            front_hub=data['front_hub'], rear_hub=data['rear_hub'], tires=data['tires']
        )
        qry_review_frameset_update = ReviewFrameset.objects.get(review=pk)

        qry_review_frameset_update.demo_frameset_frame_type.clear()
        for frameset_frame_type_id in data.getlist('frame_type'):
            qry_review_frameset_update.demo_frameset_frame_type.add(frameset_frame_type_id)

        qry_review_frameset_update.demo_frameset_wheel_size.clear()
        for frameset_wheel_size_id in data.getlist('wheel_size'):
            qry_review_frameset_update.demo_frameset_wheel_size.add(frameset_wheel_size_id)
        qry_review_frameset_update.save()

        if data['drivetrain_gears'] == "":
            data['drivetrain_gears'] = None

        ReviewDrivetrain.objects.filter(review=pk).update(
            drivetrain_gears=data['drivetrain_gears'], demo_drivetrain_gears=data['drivetrain_gears'], shift_levers=data['shift_levers'],
            front_derailleur=data['front_derailleur'], crankset=data['crankset'],
            rear_derailleur=data['rear_derailleur'], electronic_shifting=data['electronic_shifting'],
            internally_geared_hub=data['internally_geared_hub'],
            continually_variable_transmission=data['continually_variable_transmission'], cassette=data['cassette'],
            chainring=data['chainring'], belt_drive=data['belt_drive']
        )

        if data['seatpost_diameter'] == "":
            data['seatpost_diameter'] = None

        ReviewComponents.objects.filter(review=pk).update(
            headset=data['headset'], stem=data['stem'], handlebar=data['handlebar'], grips=data['grips'],
            seatpost=data['seatpost'], seatpost_diameter=data['seatpost_diameter'], demo_seatpost_diameter=data['seatpost_diameter'],
            saddle=data['saddle'], pedals=data['pedals'], front_brake=data['front_brake'], rear_brake=data['rear_brake'],
            components_brake_type=add_brake_type
        )
        qry_review_components_update = ReviewComponents.objects.get(review=pk)

        qry_review_components_update.save()
        for components_brake_type_id in data.getlist('brake_type'):
            qry_review_components_update.demo_components_brake_type.add(components_brake_type_id)
        qry_review_components_update.save()

            
        if data['systems_motor_nominal_output'] == "":
            data['systems_motor_nominal_output'] = None
        if data['systems_battery_watt_hours'] == "":
            data['systems_battery_watt_hours'] = None

        ReviewEbikeSystems.objects.filter(review=pk).update(
            systems_bike_class=add_bike_class, systems_motor_type=data['systems_motor_type'], motor=data['motor'], additional_motors=data['additional_motors'],
            systems_motor_nominal_output=data['systems_motor_nominal_output'], demo_systems_motor_nominal_output=data['systems_motor_nominal_output'], 
            display=data['display'], smart_bike=data['smart_bike'], theft_gps=data['theft_gps'],
            systems_battery_watt_hours=data['systems_battery_watt_hours'], demo_systems_battery_watt_hours=data['systems_battery_watt_hours'], 
            battery=data['battery'], additional_battery=data['additional_battery'], charger=data['charger']
        )
        qry_review_ebikesystem_update = ReviewEbikeSystems.objects.get(review=pk)

        qry_review_ebikesystem_update.demo_systems_bike_class.clear()
        for systems_bike_class_id in data.getlist('bike_class'):
            qry_review_ebikesystem_update.demo_systems_bike_class.add(systems_bike_class_id)
        qry_review_ebikesystem_update.save()

        ReviewAccessories.objects.filter(review=pk).update(
            lights=data['lights'], fenders=data['fenders'],
            front_rack=data['front_rack'], rear_rack=data['rear_rack']
        )
        if data['imageArray'] != '' and data['oldImageArray'] != '':
            new_review_images = eval(data['imageArray'])
            old_review_images = eval(data['oldImageArray'])

            for image in old_review_images:
                ReviewGalley.objects.filter(id=image['image']).update(order=image['index'])

            for new_image in new_review_images:
                if new_image:
                    qry_gallery_image = ImageGallery.objects.filter(id=new_image['image'])
                    if qry_gallery_image.exists():
                        qry_review_galley_add = ReviewGalley(image=qry_gallery_image.first(), review=qry_review_update, order=new_image['index'])
                        qry_review_galley_add.save()
        if data['delete_image_list']:
            for review_gallery_id in eval(data['delete_image_list']):
                if review_gallery_id:
                    qry_review_galley_del = ReviewGalley.objects.get(id=review_gallery_id)
                    qry_review_galley_del.delete()
        return redirect(reverse("core:review-list"))

    def get_success_url(self):
        return reverse("core:review-list")


class ReviewDeleteView(MyDeleteView):
    """
    View to delete Review
    """
    model = Review
    template_name = "core/confirm_delete.html"
    permission_required = ("core.delete_review",)

    def get_success_url(self):
        return reverse("core:review-list")


class ReviewAjaxPagination(DataTableMixin, HasPermissionsMixin, MyLoginRequiredView):
    """
    Ajax-Pagination view for Review
    """
    model = Review
    queryset = model.objects.all().order_by("-id")

    def _get_is_superuser(self, obj):
        """Get boolean column markup."""
        t = get_template("core/partials/list_boolean.html")
        return t.render({"bool_val": obj.is_superuser})

    def is_orderable(self):
        """Check if order is defined in dictionary."""
        # if self._querydict.get("order"):
        #     return True
        return True

    def _get_actions(self, obj):
        """Get actions column markup."""
        t = get_template("core/partials/list_row_actions.html")
        opts = self.model._meta
        return t.render({
            "o": obj,
            "opts": opts,
            "has_change_permission": self.has_change_permission(self.request),
            "has_delete_permission": self.has_delete_permission(self.request),
        })

    def filter_queryset(self, qs):
        """Return the list of items for this view."""
        # If a search term, filter the query
        if self.search:
            return qs.filter(
                Q(name__icontains=self.search) |
                Q(slug__icontains=self.search)
            )
        return qs

    def prepare_results(self, qs):
        """Prepare final result data here."""
        # Create row data for datatables
        data = []
        for o in qs:
            data.append(
                {
                    "id": o.id,
                    "name": o.name,
                    "create_by__full_name": o.create_by.full_name,
                    "status": o.status,
                    "actions": self._get_actions(o),
                }
            )
        return data

    def get(self, request, *args, **kwargs):
        context_data = self.get_context_data(request)
        total_filter_data = len(self.filter_queryset(self.model.objects.all().order_by("-id")))
        context_data['recordsTotal'] = len(self.model.objects.all().order_by("-id"))
        context_data['recordsFiltered'] = total_filter_data
        return JsonResponse(context_data)


@csrf_exempt
def upload_image_gallery(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image')
        data = []
        for image in images:
            image_name = image.name
            image_size = "{:.2f} KB".format(image.size/1024.0)
            image_ratio = str(get_image_dimensions(image)[0])+' by '+str(get_image_dimensions(image)[1])+' pixels'
            image_title = image_name.split('.')[0]
            qry_image_galley_add = ImageGallery(name=image_name, title=image_title, image_size=image_size, ratio=image_ratio, image=image)
            qry_image_galley_add.save()
            data.append({'id': qry_image_galley_add.id, 'title': qry_image_galley_add.title, 'url': qry_image_galley_add.thumbnail_image.url})
        return JsonResponse({
            'status': True,
            'data': data
        })
    else:
        return JsonResponse({'status': False})


def get_image_gallery(request):

        search_value = request.GET['search_value']
        page = request.GET['page']
        if search_value:
            qry_image_list = ImageGallery.objects.filter(
                Q(name__icontains=search_value) | Q(title__icontains=search_value) | Q(caption__icontains=search_value) |
                Q(alt_text__icontains=search_value) | Q(description__icontains=search_value) |
                Q(image_size__icontains=search_value) | Q(ratio__icontains=search_value)
                | Q(create_at__icontains=search_value)
            ).order_by('-id')
        else:
            qry_image_list = ImageGallery.objects.all().order_by('-id')

        qry_gallery_images_list = Paginator(qry_image_list, 50)
        try:
            gallery_images = qry_gallery_images_list.page(page)
        except PageNotAnInteger:
            gallery_images = qry_gallery_images_list.page(1)
        except EmptyPage:
            gallery_images = qry_gallery_images_list.page(qry_gallery_images_list.num_pages)

        if gallery_images.has_next():
            next_page = gallery_images.next_page_number()
        else:
            next_page = None
        data = []
        for image in gallery_images:
            data.append({
                'id': image.id,
                'title': image.title,
                'url': image.thumbnail_image.url
            })

        context = {
            "status": True,
            "data": data,
            "pagination": {
                "total": len(qry_image_list),
                "show_value": gallery_images.end_index(),
                "next_page": next_page,
            }
        }
        return JsonResponse(context)


@csrf_exempt
def gallery_image_details(request):
    if request.method == 'POST':
        qry_image_gallery = ImageGallery.objects.filter(id=request.POST['image_gallery_id'])
        if qry_image_gallery.exists():
            data = {
                'id': qry_image_gallery[0].id,
                'name': qry_image_gallery[0].name,
                'alt_text': qry_image_gallery[0].alt_text,
                'title': qry_image_gallery[0].title,
                'caption': qry_image_gallery[0].caption,
                'description': qry_image_gallery[0].description,
                'image_size': qry_image_gallery[0].image_size,
                'ratio': qry_image_gallery[0].ratio,
                'thumbnail_image': qry_image_gallery[0].thumbnail_image.url,
                'create_at': str(qry_image_gallery[0].create_at.date),

            }
            context = {
                'status': True,
                'data': data
            }
        else:
            context = {
                'status': False,
            }
    else:
        context = {
            'status': False,
        }
    return JsonResponse(context)


@csrf_exempt
def gallery_image_delete(request):
    if request.method == 'POST':
        gallery_image_id = request.POST['image_gallery_id']
        qry_gallery_image = ImageGallery.objects.filter(id=gallery_image_id)
        if qry_gallery_image.exists():
            qry_gallery_image.delete()
            context = {
                'status': True,
            }
        else:
            context = {
                'status': False,
            }
    else:
        context = {
            'status': False,
        }
    return JsonResponse(context)


@csrf_exempt
def gallery_image_edit(request):
    if request.method == 'POST':
        image_gallery_id = request.POST['image_gallery_id']
        image_gallery_alt_text = request.POST['image_gallery_alt_text']
        image_gallery_title = request.POST['image_gallery_title']
        image_gallery_caption = request.POST['image_gallery_caption']
        image_gallery_description = request.POST['image_gallery_description']
        qry_gallery_image_update = ImageGallery.objects.filter(id=image_gallery_id)
        if qry_gallery_image_update.exists():
            qry_gallery_image_update.update(
                alt_text=image_gallery_alt_text, title=image_gallery_title,caption=image_gallery_caption,
                description=image_gallery_description
            )
            context = {
                'status': True,
            }
        else:
            context = {
                'status': False,
            }
    else:
        context = {
            'status': False,
        }
    return JsonResponse(context)


@csrf_exempt
def review_slug_check(request):
    if request.method == 'POST':
        print(request.POST)
        slug = request.POST['slug'].lower()
        review_id = request.POST['review_id']
        if review_id == '':
            qry_review = Review.objects.filter(slug=slug)
        else:
            qry_review = Review.objects.filter(slug=slug).exclude(id=review_id)
        if qry_review.exists():
            context = {
                'status': True,
            }
        else:
            context = {
                'status': False,
            }
    else:
        context = {
            'status': False,
        }
    return JsonResponse(context)
