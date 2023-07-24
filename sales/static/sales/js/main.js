function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

// Display all the data from DB
function display(category_param) {
    
    // Display headline of the category
    var headline_c = document.getElementById('headline_of_category')
    headline_c.innerHTML = " "
    var li_element = category_param.getAttribute('value')
    var para = document.createElement("p")
    para.className = "headline_c";
    var node = document.createTextNode(li_element);
    para.appendChild(node)
    headline_c.appendChild(para)
    var kampaaniate_div = document.getElementById('campaign-wrapper')
    kampaaniate_div.innerHTML = " "
    var otsing = document.getElementById('otsing')
    otsing.innerHTML = " "
    if (document.getElementById('detail_general_section') != null){
        var empty_page_detail = document.getElementById('detail_general_section')
        empty_page_detail.innerHTML = ""
    }
    if (document.getElementById('messagebox') != null){
        var message = document.getElementById('messagebox')
        message.innerHTML = " "
    }
    // Use headline value to display products
    var wrapper = document.getElementById('sale-wrapper')
    wrapper.innerHTML = " "
    var url = "http://127.0.0.1:8000/sale-list/"
    data_array = []
    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
        
        var list = data
        for (var i in list){
            // Check if chosen category is connected to the item
            if (list[i].category == li_element){
                // Check store to display pictire, check if discount or old price is not null 
                var item = `
                <a class="main_href" style="text-decoration: none; color: black;"  href="/sale/${list[i].id}/"><div id="${list[i].id}" class="card_div">
                    <img ${list[i].store == "Rimi" ? 'src="https://upload.wikimedia.org/wikipedia/commons/d/da/Rimi_Baltic_Logo.png" width="70px" height="60px"' : 'src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Maxima_logo.svg/1280px-Maxima_logo.svg.png" width="70px" height="20px"'}>
                        <div class="product_container">
                            <img src=${list[i].image} width="250px" height="200px" >
                        </div>
                        <div class="price_section">
                            <p>${list[i].headline}</p>
                            <p class="soodus">${list[i].discount == 0 || list[i].discount == null  ? "" : list[i].discount}</p>
                            <p class="soodus">${list[i].new_price}</p>
                        </div>
                    </div>
                    </a>
                `          
                wrapper.innerHTML += item  

        }
        }
        
    
        
    })

}

display();

// Search function on click
function searchResults(){
    var wrapper = document.getElementById('sale-wrapper')
    wrapper.innerHTML = " "
    val = document.getElementById('search-sale').value
    var val = val.toLowerCase();
    var url = "http://127.0.0.1:8000/sale-list/"
    fetch(url)
    .then((resp) => resp.json())
    .then(function(data){
        var list = data
        for (var i in list){
            var headline = list[i].headline.toLowerCase()
            var store = list[i].store.toLowerCase()
            if(headline.includes(val) || store.includes(val)){
                var item = `
            <a class="main_href" style="text-decoration: none; color: black;"  href="/sale/${list[i].id}/"><div id="${list[i].id}" class="card_div">
                <img ${list[i].store == "Rimi" ? 'src="https://upload.wikimedia.org/wikipedia/commons/d/da/Rimi_Baltic_Logo.png" width="70px" height="60px"' : 'src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Maxima_logo.svg/1280px-Maxima_logo.svg.png" width="70px" height="20px"'}>
                    <div class="product_container">
                        <img src=${list[i].image} width="250px" height="200px" >
                    </div>
                    <div class="price_section">
                        <p>${list[i].headline}</p>
                        <p class="soodus">${list[i].discount == "0" || list[i].discount == null  ? "" : list[i].discount}</p>
                        <p class="soodus">${list[i].new_price}</p>
                    </div>
                </div>
                </a>
            `
            wrapper.innerHTML += item 

            }
        }
    })
}


// Post sale_id to Django with jQuery method
function sendData(value){

    if (document.getElementById('messagebox') != null){
        var message = document.getElementById('messagebox')
        message.innerHTML = " "
    }
    var message = document.getElementById('messagebox')
    message.innerHTML += ` <div class="alert alert-success">Toode on lisatud korvi.</div>`
    
    sale_id = value
    url = 'http://127.0.0.1:8000/saved-sales/'
    
    var data = {'pk': sale_id, 'csrfmiddlewaretoken': csrftoken};
    $.post(url, data);
   
 }


 