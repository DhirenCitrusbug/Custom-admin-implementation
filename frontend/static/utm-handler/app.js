/**
 * add UTM data to links as needed
 *
 * Hook in to events emitted by vue apps when shops are loaded and update URL to reflect current page
 * */

/** Prod */
const site = 'https://electricbikereview.com/';
/** Dev */
// const site = 'https://electricbikereview.dev/';

if(!bus){
    var bus = new Vue();
}

bus.$on('shopLoadedEvent', function(payload){
    if(payload.website){
        let currentPage = window.location.href.replace(site, '');
        if(currentPage === ''){
            payload.website = payload.website + '&utm_content=home';
            return payload;
        }else if(currentPage === 'brand'){
            payload.website = payload.website + '&utm_content=' + currentPage;
            return payload;
        }else if(currentPage === 'accessories/' || currentPage === 'guides/' || currentPage === 'compare/'){
            payload.website = payload.website + '&utm_content=' + currentPage.substring(0, currentPage.length - 1);
            return payload;
        }else{
            currentPage = currentPage.replace('brand/', '');
            currentPage = currentPage.replace('accessories/', '');
            currentPage = currentPage.replace('guides/', '');
            currentPage = currentPage.replace('compare/', '');
            currentPage = currentPage.replace('category/', '');
            if(currentPage.charAt(currentPage.length - 1) === '/'){
                currentPage = currentPage.substring(0, currentPage.length - 1);
            }
            currentPage = currentPage.split("/").join("-");

            payload.website = payload.website + '&utm_content=' + currentPage;
            return payload;
        }
    }
    return payload;
});