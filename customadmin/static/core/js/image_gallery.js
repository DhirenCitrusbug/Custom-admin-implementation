let image_extension = ['jpg', 'png', 'jpeg']
$('#image_gallery').on('change', function(ev) {
    ev.preventDefault();
    if (this.files.length > 0) {
        for (var i = 0; i < this.files.length; i++) {
            $('.page-loader').show();
            var data = new FormData();
            if(this.files[i].size < 15097152){
                var extension = this.files[i].name.substr((this.files[i].name.lastIndexOf('.') + 1)).toLowerCase();
                if (image_extension.indexOf(extension) > -1) {
                    data.append('image', this.files[i]);
                    $.ajax({
                        method: "POST",
                        url: "/customadmin/upload-image-gallery",
                        data: data,
                        contentType:false,
                        processData: false,
                        success: function (res) {
                            if(res['status'] === true){
                                image_list = res['data']
                                for(var i=0; i< image_list.length; i++){
                                    $('.gallery_image_list').prepend(`
                                        <li data-value='${image_list[i]['id']}' class='image_details selected'>
                                            <span class="check_mark"></span>
                                            <img src="${image_list[i]['url']}" alt="" title="${image_list[i]['title']}" class="img-fluid">
                                        </li>
                                    `)
                                }
                            }else{
                                alert('Some error is occur.')
                            }
                        },
                        complete: function(){
                            $('.page-loader').hide();
                        }
                    });
                }
            }
        }
        this.value = ''
    }
    $('#profile-tab').trigger('click');
});


// drag file zone
function dragOverHandler(ev) {
  console.log('File(s) in drop zone');
  ev.preventDefault();
  clear_gallery_section();
}

function dropHandler(ev) {
  console.log("File(s) dropped");
  ev.preventDefault();
  images = ev.dataTransfer.files;

  for (var i = 0; i < ev.dataTransfer.items.length; i++) {
    var data = new FormData();
     if(images[i].size < 15097152){
        var extension = images[i].name.substr((images[i].name.lastIndexOf('.') + 1)).toLowerCase();
         if (image_extension.indexOf(extension) > -1) {
            data.append('image', this.images[i]);
            $('.page-loader').show();
            $.ajax({
                method: "POST",
                url: "/customadmin/upload-image-gallery",
                data: data,
                contentType:false,
                cache: false,
                processData: false,
                async:true,
                success: function (res) {
                    if(res['status'] === true){
                        image_list = res['data']
                        console.log(image_list)
                        for(var i=0; i< image_list.length; i++){
                            $('.gallery_image_list').prepend(`
                                <li data-value='${image_list[i]['id']}' class='image_details selected'>
                                    <span class="check_mark"></span>
                                    <img src="${image_list[i]['url']}" alt="" title="${image_list[i]['title']}" class="img-fluid">
                                </li>
                            `)
                        }
                    }else{
                        alert('Some error is occur.')
                    }
                },
                complete: function(){
                    $('.page-loader').hide();
                }
            });
        }
     }
  }
  $('#profile-tab').trigger('click');
}


$('.image_gallery_open').on('click', function(){
        $('.eb_media_popup_wrapper').css('display', 'block');
        $('body').addClass('overflow_hidden');
        $('.gallery_image_list').empty();
        $('.page-loader').show();
        $.ajax({
            method: "get",
            url: "/customadmin/get-image-gallery",
            data: {'search_value': '', 'page': 1},
            dataType: 'json',
            async: true,
            success: function (res) {
                if(res['status'] === true){
                    image_list = res['data']
                    for(var i=0; i< image_list.length; i++){
                        $('.gallery_image_list').append(`
                        <li data-value='${image_list[i]['id']}' class='image_details'>
                            <span class="check_mark"></span>
                            <img src="${image_list[i]['url']}" alt="" title="${image_list[i]['title']}" class="img-fluid">
                        </li>
                        `)
                    }
                    pagination = res['pagination']
                    $('.image_gallery_recode').html(pagination['show_value']+' of '+pagination['total']+' images');
                    if(pagination['next_page'] != null){
                        $('#load_more_img_btn').css('display', 'initial');
                        $('#load_more_img_btn').data('value', pagination['next_page']);
                    }else{
                        $('#load_more_img_btn').data('value', 1);
                        $('#load_more_img_btn').css('display', 'none');
                    }

                }else{
                    alert('Some error is occur.')
                }
            },
            complete: function(){
                $('.page-loader').hide();
            }
        });
   });

   $('#load_more_img_btn').on('click', function(){
        page = $(this).data('value');
        search_value = $('#search_value').val();
        $('.page-loader').show();
        $.ajax({
            method: "get",
            url: "/customadmin/get-image-gallery",
            data: {'search_value': search_value, 'page': page},
            dataType: 'json',
            async: true,
            success: function (res) {
                if(res['status'] === true){
                    image_list = res['data']
                    for(var i=0; i< image_list.length; i++){
                        $('.gallery_image_list').append(`
                        <li data-value='${image_list[i]['id']}' class='image_details'>
                            <span class="check_mark"></span>
                            <img src="${image_list[i]['url']}" alt="" title="${image_list[i]['title']}" class="img-fluid">
                        </li>
                        `)
                    }
                    pagination = res['pagination']
                    $('.image_gallery_recode').html(pagination['show_value']+' of '+pagination['total']+' images');
                    if(pagination['next_page'] != null){
                        $('#load_more_img_btn').css('display', 'initial');
                        $('#load_more_img_btn').data('value', pagination['next_page']);
                    }else{
                        $('#load_more_img_btn').data('value', 1);
                        $('#load_more_img_btn').css('display', 'none');
                    }

                }else{
                    alert('Some error is occur.')
                }
            },
            complete: function(){
                $('.page-loader').hide();
            }
        });
   });

   $('#search_value').on('keyup', function(){
        page = $('#load_more_img_btn').data('value');
        search_value = $('#search_value').val();
        $('.page-loader').show();
        $.ajax({
            method: "get",
            url: "/customadmin/get-image-gallery",
            data: {'page': 1, 'search_value': search_value},
            dataType: 'json',
            async: true,
            success: function (res) {
                console.log(res)
                if(res['status'] === true){
                    image_list = res['data']
                    $('.gallery_image_list').empty();
                    for(var i=0; i< image_list.length; i++){
                        $('.gallery_image_list').append(`
                        <li data-value='${image_list[i]['id']}' class='image_details'>
                            <span class="check_mark"></span>
                            <img src="${image_list[i]['url']}" alt="" title="${image_list[i]['title']}" class="img-fluid">
                        </li>
                        `)
                    }
                    pagination = res['pagination']
                    $('.image_gallery_recode').html(pagination['show_value']+' of '+pagination['total']+' images');
                    if(pagination['next_page'] != null){
                        $('#load_more_img_btn').css('display', 'initial');
                        $('#load_more_img_btn').data('value', pagination['next_page']);
                    }else{
                        $('#load_more_img_btn').data('value', 1);
                        $('#load_more_img_btn').css('display', 'none');
                    }

                }else{
                    alert('Some error is occur.')
                }
            },
            complete: function(){
                $('.page-loader').hide();
            }
        });
   });


    // Close image gallery
    $('.gallery_close').on('click', function(){
        $('.eb_media_popup_wrapper').css('display', 'none');
        $('body').removeClass('overflow_hidden');
        $('.eb_mediaList_right_inner').css('display', 'none')
    });

    // Get image gallery data.
    $(document).on('click', '.image_details', function(e){
         if (e.ctrlKey != true && e.metaKey != true) {
             $(this).siblings().removeClass("selected");
             $('.eb_mediaList_right_inner').css('display', 'none')
         }
         if($(this).hasClass("selected") === true){
            $(this).removeClass('selected');
         }else{
            $(this).addClass('selected');
            image_gallery_id = $(this).data('value');
            $('.page-loader').show();
            $.ajax({
              method: "POST",
              url: "/customadmin/gallery-image-details",
              data: {'image_gallery_id': image_gallery_id},
              dataType: 'json',
              async: true,
              success: function (res) {
                if(res['status'] === true){
                    image_details = res['data']
                    $('#image_gallery_img').attr('src', image_details['thumbnail_image']);
                    $('#image_gallery_img_name').html(image_details['name']);
                    $('#image_gallery_image_date').html(image_details['create_at']);
                    $('#image_gallery_size').html(image_details['image_size']);
                    $('#image_gallery_img_ratio').html(image_details['ratio']);
                    $('#image_gallery_alt_text').val(image_details['alt_text']);
                    $('#image_gallery_title').val(image_details['title']);
                    $('#image_gallery_caption').val(image_details['caption']);
                    $('#image_gallery_description').val(image_details['description']);
                    $('#image_gallery_url').val(image_details['thumbnail_image']);
                    $('#image_gallery_id').val(image_details['id']);

                    $('.eb_mediaList_right_inner').css('display', 'block')
                }else{
                    alert("Some thing goes wrong.")
                }
              },
              complete: function(){
                $('.page-loader').hide();
              }
             });
         }
    });

    // Delete image gallery data
    $('#gallery_image_delete').on('click', function(){
          if(confirm("You are about to permanently delete this item from your site.\nThis action cannot be undone.\n'Cancel' to stop, or 'OK' to delete. ")){
            $('.page-loader').show();
            $.ajax({
              method: "POST",
              url: "/customadmin/gallery-image-delete",
              data: {'image_gallery_id': $('#image_gallery_id').val()},
              dataType: 'json',
              async: true,
              success: function (res) {
                if(res['status'] === true){
                    var image_li = $("ul").find(`[data-value='${$('#image_gallery_id').val()}']`)
                    image_li.remove()
                    $('.eb_mediaList_right_inner').css('display', 'none');
                }else{
                    alert('Image id not found, please refresh page.')
                }
              },
              complete: function(){
                $('.page-loader').hide();
              }
             });
          }
    });

    // Update image gallery data like alt_name, title, description.
    $('#gallery_image_form_submit').on('click', function(){
        $('.page-loader').show();
       $.ajax({
          method: "POST",
          url: "/customadmin/gallery-image-edit",
          data: $("#gallery_image_form").serialize(),
          dataType: 'json',
          async: true,
          cache : false,
          success: function (res) {
            console.log(res)
            if(res['status'] === true){
                alert('Successfully update image data.')
            }else{
                alert('Image id not found, please refresh page.')
            }
          },
          complete: function(){
            $('.page-loader').hide();
          }
         });
    });

    function clear_gallery_section(){
        $('.image_details').removeClass('selected');
        $('.eb_mediaList_right_inner').css('display', 'none')
    }