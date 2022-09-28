from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
import base64
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt

from .serializers import CommentSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from core.models import (Review, Pages, ReviewCategory, ReviewBrand, ReviewGeneral, ReviewFrameset, ReviewDrivetrain,
                         ReviewComponents, ReviewEbikeSystems, ReviewAccessories, ReviewHighlights, ReviewGalley, UpVote,
                         ModelYear, BikeClass, FrameType, WheelSize, BreakType, Comments, ImageGallery, UpVoteReviewHighlights,
                         User, ContactUs, VisitorHistory
                         )
from django.conf import settings
import requests
import json
import re
from django.shortcuts import redirect
from datetime import datetime
from django.views.decorators.clickjacking import xframe_options_exempt
from .utils import review_dict, brand_details_schema, category_details_schema, home_seo, comment_check
from youtubesearchpython import VideosSearch
from django.template.loader import get_template
from django.core.mail import send_mail


def add_fields(request, pk):
    if pk == 1:
        add_bike_class()
    elif pk == 2:
        add_frame_type()
    elif pk == 3:
        add_break_type()
    elif pk == 4:
        add_wheel_size()
    elif pk == 5:
        add_wieght()
    elif pk == 6:
        add_battery()
    elif pk == 7:
        add_model_year()
    elif pk == 8:
        add_gear()
    elif pk == 9:
        add_motor_nominal()
    elif pk == 10:
        add_load_capacity()
    elif pk == 11:
        add_seatpost_diameter()
    elif pk == 12:
        add_motor_nominal()
    elif pk == 13:
        check_bike_class()
    # print('--------------------')
    return True


def split_str(str):
    if "Class 200" in str:
        new_ = str.replace("Class 200", "")
        new_str = remove_class(new_)
    else:
        new_str = str.split("', '")  # space for class
    return new_str


def split_class(str):
    if "Class 200" in str:
        new_ = str.replace("Class 200", "")
        new_str = remove_class(new_)
    else:
        new_str = str.split("', ' ")  # space for class
    return new_str


def remove_class(str):
    new_str = str.split("', ' ")
    return new_str


def bike_class_split(str):
    new_str = str[2:-2]
    return new_str


def add_bike_class():
    bike_class = BikeClass.objects.all()
    add_bike = ReviewEbikeSystems.objects.all().order_by('id')
    add_general = ReviewGeneral.objects.all().order_by('id')
    
    for obj, obj_frameset in zip(add_general, add_bike):
        obj_frameset.systems_bike_class = split_class(obj.bike_class[2:-2])
        obj_frameset.save()
        qry_more = bike_class.filter(bike_class__in = split_class(obj.bike_class[2:-2]))
        for i in qry_more:
            obj_frameset.demo_systems_bike_class.add(i)


def add_frame_type():
    add_frame_ = ReviewFrameset.objects.all().order_by('id')
    frame_type = FrameType.objects.all()
    add_general = ReviewGeneral.objects.all().order_by('id')
    
    for obj, obj_frameset in zip(add_general, add_frame_):
        obj_frameset.frameset_frame_type = obj.frame_type
        obj_frameset.save()
        qry_more = frame_type.filter(frame_type__in = split_str(obj.frame_type[2:-2]))
        for i in qry_more:
            print(obj.frame_type, '============', i, '---------------------------------------', obj.id, obj_frameset.id)
            obj_frameset.demo_frameset_frame_type.add(i)
    return True


def add_break_type():
    break_type = BreakType.objects.all()
    add_general = ReviewGeneral.objects.all().order_by('id')
    add_components = ReviewComponents.objects.all().order_by('id')
    
    for obj_components, obj_generel in zip(add_components, add_general):
        obj_components.components_brake_type = obj_generel.brake_type
        obj_components.save()
        qry_more = break_type.filter(break_type__in = split_class(obj_generel.brake_type[2:-2]))
        for i in qry_more:
            obj_components.demo_components_brake_type.add(i)
            print(i, '------------------------------------', obj_generel.id)
    return True


def add_wheel_size():
    wheel_size = WheelSize.objects.all()
    add_bike = ReviewGeneral.objects.all().order_by('id')
    add_frame_ = ReviewFrameset.objects.all().order_by('id')
    
    for obj, obj_frameset in zip(add_bike, add_frame_):
        obj_frameset.frameset_wheel_size = obj.wheel_size
        print(obj.id, '======', obj_frameset.id)
        obj_frameset.save()
        if split_str(obj.wheel_size[2:-2]) != ['']:
            qry_more = wheel_size.filter(wheel_size__in = split_str(obj.wheel_size[2:-2]))
            for i in qry_more:
                obj_frameset.demo_frameset_wheel_size.add(i)
                print(i, '------------', obj_frameset.id, '===', obj.id)
    return True


def add_wieght():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_frameset = ReviewFrameset.objects.all().order_by('id')
    for obj, obj_frameset in zip(qry_review, qry_frameset):
        if obj.weight:
            obj.demo_weight = obj.weight
        else:
            obj.demo_weight = None
        obj.save()
        if obj_frameset.frameset_weight != 'None':
            obj_frameset.demo_frameset_weight = obj_frameset.frameset_weight
        else:
            obj_frameset.demo_frameset_weight = None
        obj_frameset.save()
        pass
    return True


def add_battery():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_ebike = ReviewEbikeSystems.objects.all().order_by('id')
    for obj, obj_ebike in zip(qry_review, qry_ebike):
        if obj.battery_watt_hours:
            obj.demo_battery_watt_hours = obj.battery_watt_hours
        else:
            obj.battery_watt_hours = None
        obj.save()
        if obj_ebike.systems_battery_watt_hours:
            obj_ebike.demo_systems_battery_watt_hours = obj_ebike.systems_battery_watt_hours
        else:
            obj_ebike.demo_systems_battery_watt_hours = None
        obj_ebike.save()
    return True


def add_model_year():
    qry_frame_type = list(
        Review.objects.all().values_list('model_year', flat=True))
    model_year = ModelYear.objects.all()
    add_bike = Review.objects.all()
    for i, val in zip(qry_frame_type, add_bike):
        if ',' in i:
            print("entered in ifff")
            qry_more = model_year.filter(year__in=i.split(', '))
            for j in qry_more:
                val.demo_model_year.add(j)
        else:
            if i != '':
                val.demo_model_year.add(model_year.get(year=int(i)))
                print("else save done ---------")
    return True


def add_gear():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_drivetrain = ReviewDrivetrain.objects.all().order_by('id')
    for general, drevetrain in zip(qry_review, qry_drivetrain):
        if general.gears != '':
            general.demo_gear = general.gears
        else:
            general.demo_gear = None
        general.save()
        if drevetrain.drivetrain_gears != '':
            drevetrain.demo_drivetrain_gears = drevetrain.drivetrain_gears
        else:
            drevetrain.demo_drivetrain_gears = None
        drevetrain.save()
    return True


def add_motor_nominal():
    qry_review = ReviewGeneral.objects.all().order_by('id')
    qry_drivetrain = ReviewEbikeSystems.objects.all().order_by('id')
    for general, drevetrain in zip(qry_review, qry_drivetrain):
        if general.motor_nominal_output != '':
            general.demo_motor_nominal_output = general.motor_nominal_output
        else:
            general.demo_motor_nominal_output = None
        general.save()
        if drevetrain.systems_motor_nominal_output != '':
            drevetrain.demo_systems_motor_nominal_output = drevetrain.systems_motor_nominal_output
        else:
            drevetrain.demo_systems_motor_nominal_output = None
        drevetrain.save()
    return True


def add_load_capacity():
    qry_review = ReviewFrameset.objects.all().order_by('id')
    for general in qry_review:
        if general.load_capacity != '':
            general.demo_load_capacity = general.load_capacity
        else:
            general.demo_load_capacity = None
        general.save()
    return True


def add_seatpost_diameter():
    qry_review = ReviewComponents.objects.all().order_by('id')
    for general in qry_review:
        if general.seatpost_diameter != '':
            general.demo_seatpost_diameter = general.seatpost_diameter
        else:
            general.demo_seatpost_diameter = None
        general.save()
    return True


def add_suspension_travel():
    qry_review = ReviewFrameset.objects.all().order_by('id')
    for general in qry_review:
        if general.suspension_travel != '':
            general.demo_suspension_travel = general.suspension_travel
        else:
            general.demo_suspension_travel = None
        general.save()
    return True


def check_bike_class():
    add_bike = ReviewEbikeSystems.objects.all().order_by('id')
    add_general = ReviewGeneral.objects.all().order_by('id')
    for obj_generel, obj_ebike in zip(add_general, add_bike):
        print(obj_generel.id, '----', obj_ebike.id)
        for generel_bike_class, ebike_bike_class in zip(obj_generel.demo_bike_class.all(), obj_ebike.demo_systems_bike_class.all()):
            if generel_bike_class != ebike_bike_class:
                print(obj_generel.id, '====', obj_ebike.id)
    return True


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def float_to_value(x):
    if x > 10**6-1:
        return str(x/10**6) + 'M'
    elif x > 10**3-1:
        return str(x/10**3) + 'K'
    else:
        return str(x)


def error_404_view(request, exception):
    # we add the path to the the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


@xframe_options_exempt
def shops_nearby(request):
    return render(request, 'dashboard-integration/shops-nearby/shops-nearby.html')


@xframe_options_exempt
def shops_osm(request):
    return render(request, 'dashboard-integration/shops-osm/directory-map.html')


def search_filter(request):
    search = request.GET.get('search_input')
    qry_review_data = Review.objects.filter(status='Published')
    data_model_name = list(qry_review_data.filter(Q(model_name__icontains=search) | Q(
        name__icontains=search)).order_by('-name').values_list('name', 'slug', 'brands__slug').distinct('name'))
    data_brand_name = list(qry_review_data.filter(Q(brands__name__icontains=search) | Q(
        name__icontains=search)).values_list('brands__name', 'brands__slug').distinct('brands__name'))

    context = {
        'data_model_name': data_model_name,
        'data_brand_name': data_brand_name,
    }

    return JsonResponse({"data": context, 'search': search}, safe=False)


def price_range_filter(request):
    start_price = request.GET.get('min_price')
    end_price = request.GET.get('max_price')
    if not start_price:
        start_price = 0
    if not end_price:
        end_price = max(ReviewGeneral.objects.all().values_list('msrp'))[0]
    qry_raview = Review.objects.filter(review_general_review__msrp__range=(
        int(start_price), int(end_price)), status='Published').count()
    data_dict = {
        'total_review': qry_raview,
        'max_price': end_price,
    }
    return JsonResponse(data_dict, safe=False)


def filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type, min_battery, max_battery, bike_class, 
                   suspension, min_suspension_travel, max_suspension_travel, accessories_fenders, accessories_lights,
                   accessories_racks, keywords, categories, brands, model_name, trim, page_filter_keywords):

    qry_year_review = Review.objects.filter(status='Published').order_by('-id')
    filtered_tags = []

    print(keywords, 'keywords')
    print(page_filter_keywords, 'page_filter_keywords')
    if bike_class != [] and bike_class is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__demo_bike_class__bike_class__in=bike_class)
        for class_name in bike_class:
            filtered_tags.append({"bike_class":class_name})

    # Year Filter
    if min_year != "" and min_year is not None or max_year != "" and max_year is not None:
        if min_year:
            filtered_tags.append({"min_year":int(min_year)})
        if max_year:
            filtered_tags.append({"max_year":int(max_year)})
        if min_year == None:
            min_year = min(qry_year_review.values_list(
                'demo_model_year__year', flat=True))
        if max_year == None:
            max_year = max(qry_year_review.values_list(
                'demo_model_year__year', flat=True))
        qry_year_review = qry_year_review.filter(
            demo_model_year__year__range=(min_year, max_year)).distinct('id')
        
    # Price Filter
    if min_price != "" and min_price is not None:
        qry_year_review = qry_year_review.filter(review_general_review__msrp__gte = min_price)
        filtered_tags.append({"min_price":int(min_price)})
    if max_price != "" and max_price is not None:
        qry_year_review = qry_year_review.filter(review_general_review__msrp__lte = max_price)
        filtered_tags.append({"max_price":int(max_price)})

    # Weight Filter
    if min_weight != "" and min_weight is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__demo_weight__gte=min_weight)
        filtered_tags.append({"min_weight":int(min_weight)})

    if max_weight != "" and max_weight is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__demo_weight__lte=max_weight)
        filtered_tags.append({"max_weight":int(max_weight)})

    # Motor Type Filter
    if motor_type != [] and motor_type is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__motor_type__in=motor_type)
        for types in motor_type:
            filtered_tags.append({"motor_type":types})

    # Battery Capacity Filter
    if min_battery != "" and min_battery is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__demo_battery_watt_hours__gte=min_battery)
        filtered_tags.append({"min_battery":int(min_battery)})

    if max_battery != "" and max_battery is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__demo_battery_watt_hours__lte=max_battery)
        filtered_tags.append({"max_battery":int(max_battery)})

    # Suspension Filter
    if suspension != [] and suspension is not None:
        qry_year_review = qry_year_review.filter(
            review_general_review__suspension__in=suspension)
        for suspension in suspension:
            filtered_tags.append({"suspension":suspension})

    # Suspension Travel Filter
    if min_suspension_travel != "" and min_suspension_travel is not None:
        qry_year_review = qry_year_review.filter(
            review_frameset_review__demo_suspension_travel__gte=min_suspension_travel)
        filtered_tags.append({"min_suspension_travel":int(min_suspension_travel)})

    if max_suspension_travel != "" and max_suspension_travel is not None:
        qry_year_review = qry_year_review.filter(
            review_frameset_review__demo_suspension_travel__lte=max_suspension_travel)
        filtered_tags.append({"max_suspension_travel":int(max_suspension_travel)})

    # Accessories Filter
    if accessories_fenders != "" and accessories_fenders is not None:
        qry_year_review = qry_year_review.filter(
            review_accessory_review__fenders=accessories_fenders)
        filtered_tags.append({"accessories_fenders":"Fenders"})

    if accessories_lights != "" and accessories_lights is not None:
        qry_year_review = qry_year_review.filter(
            review_accessory_review__lights=accessories_lights)
        filtered_tags.append({"accessories_lights":"Lights"})

    if accessories_racks != "" and accessories_racks is not None:
        qry_year_review = qry_year_review.filter(Q(review_accessory_review__front_rack=accessories_racks) | Q(
            review_accessory_review__rear_rack=accessories_racks))
        filtered_tags.append({"accessories_racks":"Racks"})
        
    # Keyword Filter
    print(page_filter_keywords, "-**/-*/-*/-*/-*/-/-/-*/-*/-*/*/-*/-*/-*/-*/*/*-/*-///*-/")
    if keywords != "" and keywords is not None and "," not in keywords:
        qry_year_review = qry_year_review.filter(Q(name__icontains=keywords) | Q(brands__name__icontains=keywords) | Q(model_name__icontains=keywords))    
        filtered_tags.append({"keywords":keywords})
        
    if page_filter_keywords != [] and page_filter_keywords is not None:
        for keywords in page_filter_keywords:
            qry_year_review = qry_year_review.filter(Q(name__icontains=keywords) | Q(brands__name__icontains=keywords) | Q(model_name__icontains=keywords))
            for keyword in page_filter_keywords:
                filtered_tags.append({"keywords":keyword})
    print(filtered_tags, '*-*-*-*-*-*-*-*-*-*-*')
    # Categories Filter
    if categories != [] and categories is not None:
        qry_year_review = qry_year_review.filter(categories__name__in = categories)
        for category in categories:
            filtered_tags.append({"category":category})
    
    # Brands Filter
    if brands != [] and brands is not None:
        qry_year_review = qry_year_review.filter(brands__name__in = brands)
        for brand in brands:
            filtered_tags.append({"brands":brand})
    
    # Model Name Filter
    if model_name != [] and model_name is not None:
        qry_year_review = qry_year_review.filter(model_name__in = model_name)
        for model_name in model_name:
            filtered_tags.append({"model_name":model_name})
    
    # Trim Filter
    if trim != [] and trim is not None:
        qry_year_review = qry_year_review.filter(trim__in = trim)
        for trim in trim:
            filtered_tags.append({"trim":trim})
    print(filtered_tags, '===================')
    data = {
        "filtered_tags":filtered_tags,
        "filtered_reviews":qry_year_review
    }

    return data


def more_filter(request):
    qry_year_review = Review.objects.filter(status='Published').order_by('-id')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_weight = request.GET.get('min_weight')
    max_weight = request.GET.get('max_weight')
    motor_type = request.GET.getlist('motor_type[]')
    min_battery = request.GET.get('min_battery')
    max_battery = request.GET.get('max_battery')
    bike_class = request.GET.getlist('bike_class[]')
    suspension = request.GET.getlist('suspension[]')
    min_suspension_travel = request.GET.get('min_suspension_travel')
    max_suspension_travel = request.GET.get('max_suspension_travel')
    accessories_fenders = request.GET.get('accessories_fenders')
    accessories_lights = request.GET.get('accessories_lights')
    accessories_racks = request.GET.get('accessories_racks')
    keywords = request.GET.get('keywords')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('min_price')
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brands[]')
    model_name = request.GET.getlist('model_name[]')
    trim = request.GET.getlist('trim[]')
    page_filter_keywords = request.GET.getlist("keywords[]")
    # qry_year_review = review_qry
    print("more-filter function ##################")
    qry_year_review = filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type, min_battery, max_battery, bike_class, 
                   suspension, min_suspension_travel, max_suspension_travel, accessories_fenders, accessories_lights,
                   accessories_racks, keywords, categories, brands, model_name, trim, page_filter_keywords)
    
    data_dict = {
        "total_reviews": list(qry_year_review['filtered_reviews'].distinct('id').values_list(flat=True)),
    }
    return JsonResponse(data_dict, safe=False)


def forums_data_api():
    days = 180
    url = settings.IFRAME_URL + \
        '/forums/api/threads?direction=desc&order=last_post_date&last_days={}'
    headers = {'XF-Api-Key': settings.IFRAME_API_KEY}
    response = requests.get(url.format(days), headers=headers)
    data_list = []
    if response.status_code == 200:
        forums_list = json.loads(response.text)
        for i in forums_list['threads'][:11]:
            data_dict = {}
            data_dict['title'] = i['title']
            data_dict['forum'] = i['Forum']['title']
            data_dict['forum_link'] = i['Forum']['view_url']
            data_dict['link'] = i['view_url']
            data_dict['post_date'] = datetime.fromtimestamp(i['post_date'])
            data_list.append(data_dict)
    return data_list


def brand_json(request):
    print(request.GET)
    slug = request.GET.get('slug', None)
    if slug is not None:
        qry_brand = ReviewBrand.objects.filter(slug=slug)
        if qry_brand.exists():
            qry_review_count = Review.objects.filter(
                brands=qry_brand[0].id, status='Published').count()
            # bike_brand['review_count'] = float_to_value(qry_review_count)
            data = {
                "description": qry_brand[0].description,
                "logo": str(qry_brand[0].brand_image_full.url) if qry_brand[0].brand_image_full else '',
                "title": qry_brand[0].name,
                "reviews": qry_review_count
            }
            return JsonResponse(data)
        else:
            return JsonResponse(False, safe=False)
    else:
        return JsonResponse(False, safe=False)


def dashboard_brands(request):
    qry_brand = ReviewBrand.objects.all().order_by('name')
    data = []
    for brand in qry_brand:
        data.append({
            'id': brand.id,
            'slug': brand.slug,
            'name': brand.name,
            'logo_url': brand.brand_image_full.url if brand.brand_image_full else '',
            'description': brand.description
        })
    return JsonResponse({'status': 200, 'brands': data})


def index(request):
    qry_review_bike = Review.objects.filter(status='Published').order_by('-id')
    pagination = Paginator(qry_review_bike, 24)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages+1)]
    try:
        bike_reviews = pagination.page(page)
    except PageNotAnInteger:
        bike_reviews = pagination.page(1)
    except EmptyPage:
        bike_reviews = pagination.page(pagination.num_pages)

    context = {
        'bike_review': bike_reviews,
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(home_seo(), indent=4),
    }
    return render(request, 'frontend/subpages/index.html', context)


def category_filter(request):
    category_ids = request.GET.get('categories', None)
    num_review = 24
    page = request.GET.get('page', 1)
    if category_ids != None:
        qry_featured_review = None
        featured_review_ids = []
        try:
            encoded_categroy_ids = base64.b64decode(
                category_ids).decode('ascii')
            category_id_list = list(map(int, encoded_categroy_ids.split(',')))
        except:
            return HttpResponse('<h1>404 Error</h1>')

        removed_category = [int(i) for i in request.COOKIES.get(
            'remove_category_id', '').split('%2C') if i != '']
        qry_category = ReviewCategory.objects.exclude(Q(id__in=removed_category) | Q(parent_category__in=removed_category)).filter(
            Q(id__in=category_id_list) | Q(parent_category__in=category_id_list)).order_by('-parent_category')
        parent_categories = qry_category.filter(id__in=category_id_list)

        if parent_categories.count() == 1:
            return redirect(f'/category/{parent_categories.first().slug}')

        for featured_review_category in qry_category:
            if featured_review_category.featured_review:
                featured_review = featured_review_category.featured_review.split(
                    ',')
                featured_review_ids = featured_review_ids + featured_review

        qry_category_reviews = Review.objects.exclude(categories__in=removed_category).filter(
            Q(categories__in=qry_category)).distinct('id').order_by('-id')

        if len(featured_review_ids) > 0:
            qry_featured_review = Review.objects.filter(
                id__in=featured_review_ids)
            qry_category_reviews = qry_category_reviews.filter(
                ~Q(id__in=featured_review_ids))
            num_review -= len(featured_review_ids)

        pagination = Paginator(qry_category_reviews, num_review)
        pages = [i for i in range(1, pagination.num_pages+1)]

        try:
            bike_category = pagination.page(page)
        except PageNotAnInteger:
            bike_category = pagination.page(1)
        except EmptyPage:
            bike_category = pagination.page(pagination.num_pages)

        context = {
            'category': qry_category,
            'featured_reviews': qry_featured_review,
            'reviews': bike_category,
            'total_reviews': qry_category_reviews.count(),
            'recent_forum_discussion': forums_data_api(),
            'pages': pages,
            'category_reviews': True,
        }

        return render(request, 'frontend/subpages/search_reviews.html', context)
    else:
        min_year = request.GET.get('min_year')
        max_year = request.GET.get('max_year')
        min_weight = request.GET.get('min_weight')
        max_weight = request.GET.get('max_weight')
        motor_type = request.GET.getlist('motor_type[]')
        min_battery = request.GET.get('min_battery')
        max_battery = request.GET.get('max_battery')
        bike_class = request.GET.getlist('bike_class[]')
        suspension = request.GET.getlist('suspension[]')
        min_suspension_travel = request.GET.get('min_suspension_travel')
        max_suspension_travel = request.GET.get('max_suspension_travel')
        accessories_fenders = request.GET.get('accessories_fenders')
        accessories_lights = request.GET.get('accessories_lights')
        accessories_racks = request.GET.get('accessories_racks')
        keywords = request.GET.get('keywords')
        # keywords = ''
        categories = request.GET.getlist('category[]')
        brands = request.GET.getlist('brands[]')
        model_name = request.GET.getlist('model_name[]')
        trim = request.GET.getlist('trim[]')
        # categories = request.GET.get('category').split(',') if request.GET.get('category') else None
        # brands = request.GET.get('brands').split(',') if request.GET.get('brands') else None
        # model_name = request.GET.get('model_name').split(',') if request.GET.get('model_name') else None
        # trim = request.GET.get('trim').split(',') if request.GET.get('trim') else None
        min_price = request.GET.get("min_price")
        max_price = request.GET.get("max_price")
        page_filter_keywords = request.GET.getlist("keywords[]")
        # page_filter_keywords = request.GET.get('keywords').split(',') if request.GET.get('keywords') else None
        featured_review_ids = []

        print("category-filter function ##################", accessories_racks)
        qry_review = filter_reviews(min_year, max_year, min_price, max_price, min_weight, max_weight, motor_type, min_battery, max_battery, bike_class,
                   suspension, min_suspension_travel, max_suspension_travel, accessories_fenders, accessories_lights,
                   accessories_racks, keywords, categories, brands, model_name, trim, page_filter_keywords)

        featured_review_category = list(filter(lambda ele:ele is not None, set(list(qry_review['filtered_reviews'].values_list('categories__featured_review', flat=True)))))
        for category_review in featured_review_category:
            featured_review_category = list(set(featured_review_category + category_review.split(",")))

        featured_review_brand = list(filter(lambda ele:ele is not None, set(list(qry_review['filtered_reviews'].values_list('brands__featured_review', flat=True)))))
        for brand_reaview in featured_review_brand:
            featured_review_brand = list(set(brand_reaview.split(",")))

        featured_review_ids =  featured_review_category + featured_review_brand
        featured_review_ids = [eval(i) for i in featured_review_ids]
        
        if featured_review_ids is not None:
            qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
            qry_review['filtered_reviews'] = qry_review['filtered_reviews'].filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
            num_review -= len(featured_review_ids)

        pagination = Paginator(qry_review['filtered_reviews'].distinct('id').order_by('-id'), num_review)
        pages = [i for i in range(1, pagination.num_pages+1)]

        try:
            bike_reviews = pagination.page(page)
        except PageNotAnInteger:
            bike_reviews = pagination.page(1)
        except EmptyPage:
            bike_reviews = pagination.page(pagination.num_pages)

        context = {
            'filtered_tags':qry_review['filtered_tags'],
            'featured_reviews': qry_featured_review,
            'reviews': bike_reviews,
            'total_reviews':qry_review['filtered_reviews'].count(),
            'recent_forum_discussion': forums_data_api(),
            'pages': pages,
            'search_reviews': True,
        }
        return render(request, 'frontend/subpages/search_reviews.html', context)


def category(request):
    qry_bike_category = ReviewCategory.objects.filter(parent_category=None, status='Published').annotate(total_review=Count(
        'review_category')).order_by('id').values('id', 'name', 'slug', 'short_description', 'icon_image', 'total_review')
    for bike_category in qry_bike_category:
        qry_child_bike_category = ReviewCategory.objects.filter(parent_category=bike_category['id'], status='Published').annotate(
            total_review=Count('review_category')).order_by('id').values('id', 'name', 'slug', 'short_description', 'icon_image', 'total_review')
        bike_category['child_bike_category'] = qry_child_bike_category

    context = {
        'bike_category': qry_bike_category,
        'recent_forum_discussion': forums_data_api()
    }
    return render(request, 'frontend/subpages/category-list.html', context)


def category_detail(request, cat_slug):
    num_review = 24
    qry_featured_review = None
    featured_review_ids = []
    category_id = [int(i) for i in request.COOKIES.get('remove_category_id', '').split('%2C') if i != '']
    get_prent_category = ReviewCategory.objects.filter(slug=cat_slug)

    if get_prent_category.first().parent_category is None:
        get_prent_category = ReviewCategory.objects.exclude(Q(id__in=category_id) | Q(parent_category__id__in=category_id)).filter(
            Q(slug=cat_slug) | Q(parent_category__slug=cat_slug)).order_by('-parent_category')
    else:
        get_prent_category = ReviewCategory.objects.exclude(
            Q(id__in=category_id)).filter(Q(slug=cat_slug)).order_by('-parent_category')
    if get_prent_category.count() == 0:
        return redirect('/')

    for featured_review_category in get_prent_category:
        if featured_review_category.featured_review:
            featured_review = featured_review_category.featured_review.split(
                ',')
            featured_review_ids = featured_review_ids + featured_review
    qry_category_reviews = Review.objects.exclude(categories__in=category_id).filter(Q(categories__in=get_prent_category) | Q(
        categories__parent_category__in=get_prent_category), status='Published').distinct('id').order_by('-id')
    if featured_review_ids is not None:
        qry_featured_review = Review.objects.filter(
            id__in=featured_review_ids, status='Published')
        qry_category_reviews = qry_category_reviews.filter(
            ~Q(id__in=featured_review_ids))
        num_review -= len(featured_review_ids)

    pagination = Paginator(qry_category_reviews, num_review)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages+1)]
    try:
        bike_category = pagination.page(page)
    except PageNotAnInteger:
        bike_category = pagination.page(1)
    except EmptyPage:
        bike_category = pagination.page(pagination.num_pages)

    seo_schema = category_details_schema(
        get_prent_category[0], qry_featured_review, bike_category)
    context = {
        'category': get_prent_category,
        'featured_reviews': qry_featured_review,
        'category_reviews': bike_category,
        'total_reviews': qry_category_reviews.count(),
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(seo_schema, indent=4),
    }
    return render(request, 'frontend/subpages/category-detail.html', context)


def category_count_ajax(request):
    category_id = request.GET.getlist('category_id[]')
    qry_category_reviews = Review.objects.filter(Q(categories__id__in=category_id) & Q(
        categories__parent_category=None), status='Published').distinct('id').count()
    return JsonResponse({'data': qry_category_reviews}, safe=False)


def review_detail(request, brand_slug, slug):
    qry_review = Review.objects.get(brands__slug=brand_slug, slug=slug)
    obj_review_generel = ReviewGeneral.objects.get(review=qry_review)
    obj_review_frameset = ReviewFrameset.objects.get(review=qry_review)
    obj_review_drivetrain = ReviewDrivetrain.objects.get(review=qry_review)
    obj_review_components = ReviewComponents.objects.get(review=qry_review)
    obj_review_ebikeSystems = ReviewEbikeSystems.objects.get(review=qry_review)
    obj_review_accessories = ReviewAccessories.objects.get(review=qry_review)
    qry_review_images = ReviewGalley.objects.filter(review=qry_review.id)
    qry_main_review_comments = Comments.objects.filter(
        comment_type='Review', parent_id=None, is_approved=True, comment_type_id=qry_review.id)

    videosSearch = VideosSearch(qry_review.name, limit=5)
    # print(videosSearch.result(), '-*/-*/-*/-*/-*/')
    if qry_review.youtube_video:
        video_ids = [qry_review.youtube_video]
    else:
        video_ids = []
    for video in videosSearch.result()['result']:
        if video['id'] not in video_ids:
            video_ids.append(video['id'])

    context = {
        'review': qry_review,
        'review_generel': obj_review_generel,
        'review_frameset': obj_review_frameset,
        'review_drivetrain': obj_review_drivetrain,
        'review_components': obj_review_components,
        'review_ebikeSystems': obj_review_ebikeSystems,
        'review_accessories': obj_review_accessories,
        'total_comments': qry_main_review_comments.count(),
        'review_images': qry_review_images,
        'recent_forum_discussion': forums_data_api(),
        'videos': video_ids[0:5],
        'is_first': 'True',
    }
    return render(request, 'frontend/subpages/review_detail.html', context)

@csrf_exempt
def add_new_comment(request):
# def add_new_comment(request, brand_slug, slug):
    if request.method == 'POST':
        name = request.POST.get("name", None)
        email = request.POST.get("email", None)
        description = request.POST.get("description").replace("<script>", "").replace("</script>", "")
        is_notification = request.POST.get("is_notification", False)
        comment_type_id = request.POST.get('comment_type_id')
        parent_id = request.POST.get('parent_id', None)
        user_ip = request.POST['user_ip']
        # csrf_token = request.POST.get('csrf_token')
        is_spam = comment_check(user_ip, request.META['HTTP_USER_AGENT'], name, email, description)



        new_comment_added = Comments.objects.create(ip=user_ip, name=name, email=email, description=description, comment_type='Review',
                                comment_type_id=comment_type_id, is_notification=is_notification, is_spam=is_spam, parent_id_id=parent_id)
    return JsonResponse({'data':'Done'}, safe=False)
    # return redirect('/'+brand_slug+'/'+slug+'/')


def display_comments(request):
    current_url = request.GET.get('url')
    upvote_comment = request.GET.get('upvote_comment')
    all_comments = request.GET.get('all_comments', 'False')
    is_upvoted = request.GET.get('is_upvoted')
    review_brand_and_slug = current_url[1:-1].split('/')
    comment_formating = request.GET.get('comment_formating', 'newest_first')
    user_ip = request.GET.get('ip')

    review_obj = Review.objects.get(slug=review_brand_and_slug[1],brands__slug=review_brand_and_slug[0])
    qry_main_review_comments = Comments.objects.filter(
        comment_type='Review', is_approved=True, comment_type_id=review_obj.id).annotate(upvote_count = Count('upvote__comment_id'))
    
    if comment_formating == 'newest_first':
        qry_main_review_comments = qry_main_review_comments.order_by('-create_at')
    if comment_formating == 'most_valuable':
        qry_main_review_comments = qry_main_review_comments.order_by('-upvote_count')
    
    if is_upvoted == 'true':
        add_comment_upvote = UpVote.objects.create(comment_id_id=upvote_comment, ip=user_ip)
    if is_upvoted == 'false':
        remove_comment_upvote = UpVote.objects.filter(comment_id_id=upvote_comment, ip=user_ip).delete()
        
    upvoted_comments = list(UpVote.objects.filter(ip=user_ip).values_list('comment_id', flat=True))
     
    comments = []
    for replied_comments in qry_main_review_comments.filter(parent_id=None):
        serializer = CommentSerializer(replied_comments)
        comments.append(serializer.data)
        
    if all_comments != 'True' and all_comments == 'False':
        comments = comments[:2]
        
    if all_comments == 'True' and all_comments != 'False':
        comments = comments[:]
        
    qry_user_admin = list(User.objects.values_list('email', flat=True))

    context = {
        'review_comments': comments,
        'upvoted_comments': upvoted_comments,
        'admin_emails': qry_user_admin,
    }
    
    return render(request,'frontend/include/replied_comments.html', context)


def display_sub_comments(request):
    parentid = request.GET.get('parent_comment_id')
    is_sub_comment = request.GET.get('is_sub_comment')
    user_ip = request.GET.get('ip')
    
    qry_comments = Comments.objects.filter(comment_type='Review', is_approved=True, parent_id=parentid)
    
    comments = []
    for replied_comments in qry_comments.annotate(upvote_count = Count('upvote__comment_id')).order_by('-upvote_count'):
        serializer = CommentSerializer(replied_comments)
        comments.append(serializer.data)
    
    # user_ip = json.loads(requests.get('https://api.ipify.org/?format=json').text)['ip']
    upvoted_comments = list(UpVote.objects.filter(ip=user_ip).values_list('comment_id', flat=True))
    
    if is_sub_comment == 'True':
        comments = comments
    if is_sub_comment == 'False':
        comments = comments[2:]
        
    qry_user_admin = list(User.objects.values_list('email', flat=True))
        
    context = {
       'review_comments': comments,
       'upvoted_comments': upvoted_comments,
       'is_sub_comment': is_sub_comment,
       'admin_emails': qry_user_admin,
    }
    
    return render(request,'frontend/include/replied_comments.html', context)


@csrf_exempt
def get_review_highlights(request):
    if request.method == 'POST':
        live_url = request.POST['live_url'].split('/')
        user_ip = request.POST['ip']
        qry_review = Review.objects.get(brands__slug=live_url[-3], slug=live_url[-2])

        qry_review_highlights = ReviewHighlights.objects.filter(review=qry_review).annotate(
            upvote_count=Count('upvotereviewhighlights__review_highlight_id')
        ).order_by('-upvote_count')

        qry_upvote_list = UpVoteReviewHighlights.objects.filter(ip=user_ip).values_list('review_highlight_id', flat=True)

        t = get_template("frontend/include/highlights.html")
        response = t.render({
            'review_highlights': qry_review_highlights,
            'upvote_list': qry_upvote_list,
        })
        context = {
            'status': True,
            'message': "Upvote added in highlights.",
            'data': response
        }
    else:
        context = {
            'status': False,
            'message': "Get method not allowed."
        }
    return JsonResponse(context)


@csrf_exempt
def highlights_update_vote(request):
    if request.method == 'POST':
        highlights_id = request.POST['highlights_id']
        ip = request.POST['ip']
        qry_highlights = ReviewHighlights.objects.filter(id=highlights_id)
        if qry_highlights.exists():
            qry_upvote = UpVoteReviewHighlights.objects.filter(ip=ip, review_highlight_id=qry_highlights[0])
            if not qry_upvote.exists():
                qry_highlights_upvote = UpVoteReviewHighlights(ip=ip, review_highlight_id=qry_highlights[0])
                qry_highlights_upvote.save()
                change = True
            else:
                qry_upvote.delete()
                change = False
            context = {
                'status': True,
                'message': "Upvote added in highlights.",
                'change': change
            }
        else:
            context = {
                'status': False,
                'message': "Highlights not found."
            }
    else:
        context = {
            'status': False,
            'message': "Get method not allowed."
        }
    return JsonResponse(context)


def get_category(request, cat_slug):
    qry_category = ReviewCategory.objects.filter(slug=cat_slug)
    if qry_category.exists():
        qry_review = Review.objects.filter(categories=qry_category[0])
        category_schema = {
            "@context": "http://schema.org",
            "@type": "CollectionPage",
            "@id": "https://electricbikereview.com/"+qry_category[0].slug+"/#WebPage",
            "mainEntity": {
                "@type": "ItemList",
                        "itemListElement": [
                        ]
            },
            "isPartOf": {
                "@type": "WebSite",
                "@id": "https://electricbikereview.com/#WebSite",
                "name": "ElectricBikeReview.com",
                "url": "https://electricbikereview.com/"
            },
            "name": qry_category[0].name,
            "about": qry_category[0].name+" Electric Bike Reviews",
            "description": qry_category[0].name+" Electric Bike Reviews",
            "publisher": {
                "@type": "Organization",
                "@id": "https://electricbikereview.com/#Organization",
                "name": "Electric Bike Review",
                "url": "https://electricbikereview.com/"
            },
            "breadcrumb": {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "item": {
                            "@id": "https://electricbikereview.com",
                            "name": "Home",
                            "url": "https://electricbikereview.com"
                        }
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "item": {
                            "@id": "https://electricbikereview.com/category/bikes/",
                            "name": "Reviews",
                            "url": "https://electricbikereview.com/category/bikes/"
                        }
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "item": {
                            "@id": "https://electricbikereview.com/category/"+qry_category[0].slug+"/",
                            "name":"Kids Electric Bike Reviews",
                            "url":"https://electricbikereview.com/category/"+qry_category[0].slug+"/"
                        }
                    }
                ]
            }
        }
        for review in qry_review:
            qry_review_highlight = ReviewHighlights.objects.filter(
                review=review)
            category_schema['mainEntity']['itemListElement'].append(
                {
                    "@context": "https://schema.org/",
                    "@type": "Product",
                    "name": review.name,
                    "image": str(review.featured_image),
                    "description": "The "+review.model_name+" is an electric bike manufactured by "+review.brands.all()[0].name,
                    "brand": {
                                "@type": "Brand",
                                "@id": "https://electricbikereview.com/brand/"+review.brands.all()[0].slug+"/#Brand",
                                "name": review.brands.all()[0].name,
                        "url": "https://electricbikereview.com/brand/"+review.brands.all()[0].slug+"/",
                        "logo": str(review.brands.all()[0].brand_image_full),
                        "description": review.brands.all()[0].description
                    },
                    "model": review.model_name,
                    "review": {
                        "@type": "Review",
                        "@id": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/#Review",
                        "name": review.name,
                        "url": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/",
                        "headline": review.name,
                        "reviewBody": ".".join([rh.highlight for rh in qry_review_highlight]),
                        "video": "https://youtube.com/watch?v="+review.youtube_video,
                        "commentCount": "",
                        "author": {
                                        "@type": "Person",
                                        "@id": "https://electricbikereview.com/#Court",
                                               "name": "Court Rye",
                                               "url": "https://electricbikereview.com/",
                                        "affiliation": {
                                            "@type": "Organization",
                                            "@id": "https://electricbikereview.com/#Organization",
                                            "name": "Electric Bike Review",
                                                    "url": "https://electricbikereview.com/"
                                        }
                        },
                        "contributor": {
                            "@type": "Person",
                            "@id": "https://electricbikereview.com/#Tyson",
                            "name": "Tyson Roehrkasse",
                            "url": "https://twirltech.solutions/",
                            "affiliation": {
                                "@type": "Organization",
                                "@id": "https://electricbikereview.com/#Organization",
                                "name": "Electric Bike Review",
                                "url": "https://electricbikereview.com/"
                            }
                        },
                        "publisher": {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        },
                        "datePublished": review.publish_date.strftime("%b %d, %Y"),
                        "sameAs": "https://electricbikereview.com/"+review.brands.all()[0].slug+"/"+review.slug+"/"
                    }
                }
            )
    context = {
        'category_details': qry_category,
        'category_schemas': json.dumps(category_schema, indent=4)
    }
    return render(request, 'frontend/review_seo.html', context)
    # return HttpResponse("<h4>This "+str(cat_slug)+" category list page.</h4>")


def brand(request):
    brand_dict = {}
    for i in range(65, 91):
        qry_bike_brand = ReviewBrand.objects.filter(name__startswith=chr(i), parent_brand=None, status='Published').order_by('name').values(
            'id', 'name', 'slug', 'brand_image_web', 'brand_image_grayscale_web', 'brand_image_darkmode_web'
        )
        data = []
        for bike_brand in qry_bike_brand:
            qry_review_count = Review.objects.filter(
                categories=bike_brand['id'], status='Published').count()
            bike_brand['review_count'] = float_to_value(qry_review_count)
            data.append(bike_brand)
        brand_dict[chr(i)] = data
    # print(brand_dict)
    context = {
        'bike_brands': brand_dict,
        'recent_forum_discussion': forums_data_api(),
    }
    return render(request, 'frontend/subpages/brand-list.html', context)


def brand_details(request, brand_slug):
    """
                    Get single Brand data with particular brand review.
    """
    num_review = 24
    qry_featured_review = None
    qry_brand = get_object_or_404(ReviewBrand, slug=brand_slug)
    featured_review = qry_brand.featured_review.split(
        ',') if qry_brand.featured_review else None

    qry_review = Review.objects.filter(
        brands=qry_brand, status='Published').order_by('-id')
    total_review = qry_review.count()
    if featured_review is not None:
        qry_featured_review = Review.objects.filter(
            id__in=featured_review, status='Published')
        qry_review = qry_review.filter(~Q(id__in=featured_review))
        num_review -= len(featured_review)

    pagination = Paginator(qry_review, num_review)
    page = request.GET.get('page', 1)
    pages = [i for i in range(1, pagination.num_pages + 1)]

    try:
        review_list = pagination.page(page)
    except PageNotAnInteger:
        review_list = pagination.page(1)
    except EmptyPage:
        review_list = pagination.page(pagination.num_pages)
    seo_schema = brand_details_schema(
        qry_brand, qry_featured_review, review_list)
    context = {
        'brand': qry_brand,
        'featured_reviews': qry_featured_review,
        'reviews': review_list,
        'total_reviews': total_review,
        'recent_forum_discussion': forums_data_api(),
        'pages': pages,
        'seo_schema': json.dumps(seo_schema, indent=4),
    }
    return render(request, 'frontend/subpages/brand-detail.html', context)


def review_page(request, brand, slug):
    qry_review = Review.objects.filter(slug=slug)
    if qry_review.exists():
        category = qry_review[0].categories.all().values()
        brand = qry_review[0].brands.all().values()
        qry_review_highlight = ReviewHighlights.objects.filter(
            review=qry_review[0])
        review_data = {
            'id': qry_review[0].id,
            'review_name': qry_review[0].name,
            'review_slug': qry_review[0].slug,
            'meta_title': qry_review[0].meta_title,
            'category': category,
            'brand': brand,
            'review_featured_image': 'https://ebr-dev-bucket.s3.amazonaws.com/'+str(qry_review[0].featured_image),
            'review_featured_image_thumbnail': 'https://ebr-dev-bucket.s3.amazonaws.com/'+str(qry_review[0].featured_image_thumbnail),
            'description': qry_review[0].description,
            'model_name': qry_review[0].model_name,
            'model_year': qry_review[0].model_year,
            'trim': qry_review[0].trim,
            'review_general': ReviewGeneral.objects.get(review=qry_review[0].id),
            'review_frameset': ReviewFrameset.objects.get(review=qry_review[0].id),
            'review_drivetrain': ReviewDrivetrain.objects.get(review=qry_review[0].id),
            'review_components': ReviewComponents.objects.get(review=qry_review[0].id),
            'review_ebike_systems': ReviewEbikeSystems.objects.get(review=qry_review[0].id),
            'review_accessory': ReviewAccessories.objects.get(review=qry_review[0].id),
            'review_highlights': ReviewHighlights.objects.filter(review=qry_review[0].id),
            'review_gallery': ReviewGalley.objects.filter(review=qry_review[0].id).order_by('order'),
            'schema': json.dumps({
                "@context": "http://schema.org",
                "@type": "WebPage",
                "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/#WebPage",
                "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                "name": qry_review[0].name,
                "mainEntity": {
                    "@type": "Review",
                    "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"//#Review",
                    "name": qry_review[0].name,
                    "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                    "itemReviewed":
                            {
                                "@type": "Product",
                                "name": qry_review[0].name,
                                "image": "https://ebr-dev-bucket.s3.amazonaws.com/"+str(qry_review[0].featured_image),
                                "description": striphtml(qry_review[0].description)[:100],
                                "brand":
                                {
                                    "@type": "Brand",
                                    "@id": "https://electricbikereview.com/brand/"+brand[0]['slug']+"/#Brand",
                                    "name": brand[0]['name'],
                                    "url": "https://electricbikereview.com/brand/"+brand[0]['slug']+"/",
                                    "logo": "https://ebr-dev-bucket.s3.amazonaws.com/"+brand[0]['brand_image_full'],
                                    "description": brand[0]['description']
                                },
                                "model": qry_review[0].model_name,
                                "review":
                                {
                                    "@type": "Review",
                                    "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"//#Review",
                                    "name": qry_review[0].name,
                                    "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                                }
                    },
                    "headline": qry_review[0].name,
                    "reviewBody": ".".join([rh.highlight for rh in qry_review_highlight]),
                    "commentCount": "0",
                    "author":
                    {
                                "@type": "Person",
                                "@id": "https://electricbikereview.com/#Court",
                                "name": "Court Rye",
                                "url": "https://electricbikereview.com/",
                                "affiliation":
                                {
                                    "@type": "Organization",
                                    "@id": "https://electricbikereview.com/#Organization",
                                    "name": "Electric Bike Review",
                                    "url": "https://electricbikereview.com/"
                                }

                    },
                    "contributor":
                    {
                                "@type": "Person",
                                "@id": "https://electricbikereview.com/#Tyson",
                                "name": "Tyson Roehrkasse",
                                "url": "https://twirltech.solutions/",
                                "affiliation":
                                {
                                    "@type": "Organization",
                                    "@id": "https://electricbikereview.com/#Organization",
                                    "name": "Electric Bike Review",
                                    "url": "https://electricbikereview.com/"
                                }
                    },
                    "publisher":
                    {
                                "@type": "Organization",
                                "@id": "https://electricbikereview.com/#Organization",
                                "name": "Electric Bike Review",
                                "url": "https://electricbikereview.com/"
                    },
                    "datePublished": qry_review[0].publish_date.strftime("%b %d, %Y"),
                    "dateModified": qry_review[0].update_at.strftime("%b %d, %Y"),
                    "sameAs": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                },
                "isPartOf":
                {
                    "@type": "WebSite",
                    "@id": "https://electricbikereview.com/#WebSite",
                    "name": "ElectricBikeReview.com",
                            "url": "https://electricbikereview.com/"
                },
                "description": qry_review[0].name,
                "about": qry_review[0].name,
                "publisher": {
                    "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                },
                "breadcrumb":
                {
                    "@type": "BreadcrumbList",
                    "itemListElement":
                    [
                        {
                            "@type": "ListItem",
                            "position": 1,
                            "item": {
                                "@id": "https://electricbikereview.website",
                                "name": "Home",
                                "url": "https://electricbikereview.website"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 2,
                            "item": {
                                "@id": "https://electricbikereview.website/category/bikes/",
                                "name": "Reviews",
                                "url": "https://electricbikereview.website/category/bikes/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "item": {
                                "@id": "https://electricbikereview.website/brand/",
                                "name": "Brands",
                                "url": "https://electricbikereview.website/brand/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 4,
                            "item": {
                                "@id": "https://electricbikereview.website/brand/"+brand[0]['slug']+"/",
                                "name": brand[0]['name'],
                                "url": "https://electricbikereview.website/brand/"+brand[0]['slug']+"/"
                            }
                        },
                        {
                            "@type": "ListItem",
                            "position": 5,
                            "item": {
                                "@id": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/",
                                "name": qry_review[0].name,
                                "url": "https://electricbikereview.website/"+brand[0]['slug']+"/"+qry_review[0].slug+"/"
                            }
                        }
                    ]
                }
            }, indent=4)
        }
        context = {
            'review_details': review_data
        }
        return render(request, 'frontend/review_seo.html', context)
    else:
        return HttpResponse("done...")


def compare(request):
    compare_review_ids = [int(i) for i in request.COOKIES.get('id', '').split('%2C') if i != '']
    qry_category_featured_review_list = ReviewCategory.objects.filter(~Q(featured_review=None)).values_list('featured_review', flat=True)
    qry_brand_featured_review_list = ReviewBrand.objects.filter(~Q(featured_review=None)).values_list('featured_review', flat=True)
    featured_review_list = []
    for featured_review in qry_category_featured_review_list:
        featured_review_list.extend(featured_review.split(','))
    for featured_review in qry_brand_featured_review_list:
        featured_review_list.extend(featured_review.split(','))
    qry_featured_review = Review.objects.filter(id__in=set(featured_review_list))
    if len(compare_review_ids) > 0:
        qry_review = Review.objects.filter(id__in=compare_review_ids)  # .values('id', 'name', 'slug', 'brands__name', 'review_general_review__msrp', 'review_general_review__bike_class', 'review_general_review__demo_bike_class__all', 'review_general_review__frame_type', 'review_general_review__demo_frame_type', 'review_general_review__suspension', 'review_general_review__wheel_size', 'review_general_review__demo_wheel_size', 'review_general_review__gears', 'review_general_review__demo_gear', 'review_general_review__brake_type', 'review_general_review__demo_brake_type', 'review_general_review__motor_type', 'review_general_review__motor_nominal_output', 'review_general_review__demo_motor_nominal_output', 'review_general_review__battery_watt_hours', 'review_general_review__demo_battery_watt_hours', 'review_general_review__demo_weight', 'review_general_review__weight', )
        print(compare_review_ids)
        context = {
            'review_list': list(qry_review),
            'featured_reviews': qry_featured_review,
        }
        return render(request, 'frontend/subpages/compare.html', context)
    else:
        context = {
            'featured_reviews': qry_featured_review,
        }
        return render(request, 'frontend/subpages/compare.html', context)


def page_view(request, page_slug):
    filtered_min_price = request.GET.get('page_filter_min_price')
    filtered_max_price = request.GET.get('page_filter_max_price')
    filtered_min_year = request.GET.get('page_filter_min_year')
    filtered_max_year = request.GET.get('page_filter_max_year')
    filtered_brands = request.GET.getlist('page_filter_brands')

    num_review = 12
    qry_page = get_object_or_404(Pages, slug=page_slug)
    qry_reviews = Review.objects.filter(status='Published').order_by('-id')
    qry_categories = ReviewCategory.objects.filter(status='Published').order_by('id')
    qry_brand = ReviewBrand.objects.filter(status='Published').order_by('id')
    featured_review_ids = []
    if qry_page:
        if qry_page.is_filter == True:
            if qry_page.filter_type == True:
                qry_reviews = qry_reviews.filter(name__icontains = qry_page.search_text)
                
                featured_review_category = list(filter(lambda ele:ele is not None, set(list(qry_categories.values_list('featured_review', flat=True)))))
                for category_review in featured_review_category:
                    featured_review_category = list(set(featured_review_category + category_review.split(",")))

                featured_review_brand = list(filter(lambda ele:ele is not None, set(list(qry_brand.values_list('featured_review', flat=True)))))
                for brand_reaview in featured_review_brand:
                    featured_review_brand = list(set(brand_reaview.split(",")))

                featured_review_ids =  featured_review_category + featured_review_brand
                featured_review_ids = [eval(i) for i in featured_review_ids]
                
                if featured_review_ids is not None:
                    qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
                    qry_reviews = qry_reviews.filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
                    num_review -= len(featured_review_ids)

            else:
                print(type(qry_page.model_name) , 'model_name', qry_page.trim, 'trim', qry_page.accessories, 'accessories')
                if qry_page.min_year or qry_page.max_year:
                    qry_reviews = qry_reviews.filter(demo_model_year__year__range=(int(qry_page.min_year), int(qry_page.max_year))).distinct('id')
                    print('year', len(qry_reviews))

                if qry_page.brands.all().count() > 0:
                    qry_reviews = qry_reviews.filter(brands__in=qry_page.brands.all())
                    qry_brand = qry_brand.filter(id__in=qry_page.brands.all())
                    print('brand', len(qry_reviews))
                    
                if qry_page.categories.all().count() > 0:
                    qry_reviews = qry_reviews.filter(categories__in=qry_page.categories.all())
                    qry_categories = qry_categories.filter(id__in=qry_page.categories.all())
                    print('category', len(qry_reviews))
                
                if qry_page.model_name != '[]':
                    qry_page.model_name = qry_page.model_name[2:-2].split("', '")
                    qry_reviews = qry_reviews.filter(model_name__in = qry_page.model_name)
                    print('model-name', len(qry_reviews))

                if qry_page.trim != '[]':
                    qry_page.trim = qry_page.trim[2:-2].split("', '")
                    qry_reviews = qry_reviews.filter(trim__in = qry_page.trim)
                    print('trim', len(qry_reviews))
                    
                if qry_page.min_price or qry_page.max_price:
                    min_price = qry_page.min_price
                    max_price = qry_page.max_price
                    if qry_page.min_price == None:
                        min_price = min(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                    if qry_page.max_price == None:
                        max_price = max(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                    qry_reviews = qry_reviews.filter(review_general_review__msrp__range=(min_price, max_price)).distinct('id')
                    print('price', len(qry_reviews))
                
                if qry_page.suspension != "":
                    qry_reviews = qry_reviews.filter(review_general_review__suspension=qry_page.suspension)
                    print('suspension', len(qry_reviews))
                    
                if qry_page.accessories != '[]':
                    qry_page.accessories = qry_page.accessories[2:-2].split("', '")
                    light_accessories = "None"
                    fenders_accessories = "None"
                    front_rack_accessories = "None"
                    rear_rack_accessories = "None"
                    if 'Lights' in qry_page.accessories:
                        light_accessories = 'Yes'
                        print('Lights')
                        qry_reviews = qry_reviews.filter(review_accessory_review__lights=light_accessories)
                    if 'Fenders' in qry_page.accessories:
                        fenders_accessories = 'Yes'
                        print('Fenders')
                        qry_reviews = qry_reviews.filter(review_accessory_review__fenders=fenders_accessories)
                    if 'Front Rack' in qry_page.accessories or 'Rear Rack' in qry_page.accessories:
                        front_rack_accessories = 'Yes'
                        rear_rack_accessories = 'Yes'
                        print('Rack')
                        qry_reviews = qry_reviews.filter(Q(review_accessory_review__front_rack=front_rack_accessories) | Q(review_accessory_review__rear_rack=rear_rack_accessories))
                    print('accessories', len(qry_reviews))
                
                if qry_page.motor_type:
                    qry_reviews = qry_reviews.filter(review_general_review__motor_type=qry_page.motor_type)
                    print('Motor Type', len(qry_reviews))
                    
                if qry_page.min_battery_capacity:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_battery_watt_hours__gte=qry_page.min_battery_capacity)
                    print('Min Battery Capacity', len(qry_reviews))
                if qry_page.max_battery_capacity:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_battery_watt_hours__lte=qry_page.max_battery_capacity)
                    print('Max Battery Capacity', len(qry_reviews))
                    
                if qry_page.min_weight:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_weight__gte=qry_page.min_weight)
                    print('Min Weight', len(qry_reviews))
                if qry_page.max_weight:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_weight__lte=qry_page.max_weight)
                    print('Max Weight', len(qry_reviews))
                    
                if qry_page.bike_class:
                    qry_reviews = qry_reviews.filter(review_general_review__demo_bike_class__bike_class__icontains=qry_page.bike_class)
                    print('Bike Class', len(qry_reviews))
                    
                if qry_page.keyword:
                    qry_page.keyword = qry_page.keyword.split(",")
                    qry_reviews = qry_reviews.filter(Q(name__in=qry_page.keyword) | Q(brands__name__in=qry_page.keyword) | Q(model_name__in=qry_page.keyword))
                    # qry_reviews = qry_reviews.filter(Q(name__icontains=qry_page.keyword) | Q(brands__name__icontains=qry_page.keyword) | Q(model_name__icontains=qry_page.keyword))
                    print('Keyword', len(qry_reviews))
                
                print(qry_reviews.count(), '====')
                        
                featured_review_category = list(filter(lambda ele:ele is not None, set(list(qry_categories.values_list('featured_review', flat=True)))))
                for category_review in featured_review_category:
                    featured_review_category = list(set(featured_review_category + category_review.split(",")))

                featured_review_brand = list(filter(lambda ele:ele is not None, set(list(qry_brand.values_list('featured_review', flat=True)))))
                for brand_reaview in featured_review_brand:
                    featured_review_brand = list(set(brand_reaview.split(",")))

                featured_review_ids =  featured_review_category + featured_review_brand
                featured_review_ids = [eval(i) for i in featured_review_ids]
                
                if featured_review_ids is not None:
                    qry_featured_review = Review.objects.filter(id__in=featured_review_ids, status='Published')
                    qry_reviews = qry_reviews.filter(~Q(id__in=featured_review_ids)).distinct('id').order_by('-id')
                    num_review -= len(featured_review_ids)
                
            if filtered_min_price or filtered_max_price:
                if not filtered_min_price:
                    filtered_min_price = min(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                if not filtered_max_price:
                    filtered_max_price = max(list(qry_reviews.values_list('review_general_review__msrp', flat=True)))
                qry_reviews = qry_reviews.filter(review_general_review__msrp__range=(int(filtered_min_price), int(filtered_max_price)))
            print('max prive', qry_reviews.count())
            if filtered_min_year or filtered_max_year:
                if not filtered_min_year:
                    filtered_min_year = min(list(qry_reviews.values_list('demo_model_year__year', flat=True)))
                if not filtered_max_year:
                    filtered_max_year = max(list(qry_reviews.values_list('demo_model_year__year', flat=True)))
                qry_reviews = qry_reviews.filter(demo_model_year__year__range=(int(filtered_min_year), int(filtered_max_year)))
            print('max year', qry_reviews.count())
            if filtered_brands:
                qry_reviews = qry_reviews.filter(brands__name__in=filtered_brands)
            print('brands....', qry_reviews.count())     
            pagination = Paginator(qry_reviews, num_review)
            page = request.GET.get('page', 1)
            pages = [i for i in range(1, pagination.num_pages+1)]
            try:
                bike_reviews = pagination.page(page)
            except PageNotAnInteger:
                bike_reviews = pagination.page(1)
            except EmptyPage:
                bike_reviews = pagination.page(pagination.num_pages)

            context = {
                'featured_reviews': qry_featured_review,
                'page_details': qry_page,
                'bike_review': bike_reviews,
                'brands':qry_brand,
                'total_reviews': qry_reviews.count()+qry_featured_review.count(),
                'pages': pages,
                'recent_forum_discussion': forums_data_api(),
            }
                
        else:
            context = {
            'page_details': qry_page,
            'recent_forum_discussion': forums_data_api(),
            }

        return render(request, 'frontend/subpages/common_page.html', context)
    else:
        return HttpResponse("<h1>Page not found.</h1>")


@csrf_exempt
def send_message(request):
# def send_message(request, page_slug):
    if request.method == 'POST':
        name = request.POST.get('contact_us_name')
        email = request.POST.get('contact_us_email')
        description = request.POST.get('contact_us_description').replace("<script>", "").replace("</script>", "")
        new_description = re.sub("[^A-Za-z0-9]", "", description)
        is_spam = comment_check('', request.META['HTTP_USER_AGENT'], name, email, new_description)
        qry_contactus = ContactUs(name=name, email=email, message=description, is_spam=is_spam)
        qry_contactus.save()
        send_mail('Automated Response - Contact Form Submission Received', 'Greetings! \n This is an auto-generated response to let you know that we received your Contact Us form submission on ElectricBikeReview.com. A member of our support team will be in contact with you soon!', 'info@electricbikereview.com', [email])
        if not is_spam:
            t = get_template("frontend/include/contact_us_email.html")
            html_message = t.render({
                'name': name,
                'email': email,
                'description': description,
            })
            # print(html_message)
            send_mail('Fwd: EBR Contact Form Submission from {}'.format(name), '', 'info@electricbikereview.com', ['vicky@mailinator.com'], html_message=html_message)

    return JsonResponse({"data":"Done"}, safe=False)
    # return redirect('/'+page_slug+'/')


def visitor_history(request):
    ip = request.GET['ip']
    type = request.GET['type']
    type_name = request.GET['type_name']
    type_url = request.GET['type_url']
    qry_visitor_history = VisitorHistory(ip=ip, type=type, type_name=type_name, type_url=type_url)
    qry_visitor_history.save()
    return JsonResponse(True, safe=True)


def review_seo(request):
    qry_review = Review.objects.all().order_by('id').values('id', 'name', 'slug', 'meta_title', 'publish_date', 'description', 'featured_image', 'featured_image_web',
                                                            'model_name', 'model_year', 'trim', 'categories__name', 'brands__name', 'brands__slug', 'more_details', 'review_general_review__msrp').distinct('id')
    data = []
    for review in qry_review:
        review["schema"] = json.dumps({
            "@context": "http://schema.org/",
            "@type": "Review",
            "@id": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/#Review",
            "url": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/",
            "itemReviewed":
            {
                "@type": "Product",
                "name": review['name'],
                "image": ''+review['featured_image'],
                "description": striphtml(review['description'])[:150],
                "model": review['model_name'],
                "review":
                {
                    "@type": "Review",
                        "@id": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/#Review",
                        "name": review['name'],
                        "url": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/"
                }
            },
            "headline": review['name'],
            "author":
            {
                "@type": "Person",
                    "@id": "https://electricbikereview.com/#Court",
                    "name": "Court Rye",
                    "url": "https://electricbikereview.com/",
                    "affiliation":
                        {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        }

            },
            "contributor":
            {
                "@type": "Person",
                    "@id": "https://electricbikereview.com/#Tyson",
                    "name": "Tyson Roehrkasse",
                    "url": "https://twirltech.solutions/",
                    "affiliation":
                        {
                            "@type": "Organization",
                            "@id": "https://electricbikereview.com/#Organization",
                            "name": "Electric Bike Review",
                            "url": "https://electricbikereview.com/"
                        }
            },
            "publisher":
            {
                "@type": "Organization",
                    "@id": "https://electricbikereview.com/#Organization",
                    "name": "Electric Bike Review",
                    "url": "https://electricbikereview.com/"
            },
            "datePublished": review['publish_date'].strftime("%b %d, %Y"),
            "sameAs": "https://electricbikereview.com/"+review['brands__name']+"/"+review['slug']+"/"
        }, indent=4)
        data.append(review)
    context = {
        'reviews': data
    }
    return render(request, 'frontend/home_seo.html', context)
