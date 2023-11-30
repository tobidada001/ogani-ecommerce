
    $(document).ready(function(){



    if (localStorage.getItem("cart") == null) {
          cart = {};
    } else {  cart = JSON.parse(localStorage.getItem("cart"));
    }
        loadData(cart) // Set the number of items in cart on the "Cart" icons in navbar
        loadcartitems() // Load the items in cart page
        loadnavbartotal() // Load the total amount of cart items in cart on the nav bar
    
    $('.addtocart').on('click', function(e){
       
      var curpid = e.target.dataset.pid;
      var name = e.target.dataset.name;
      var price = e.target.dataset.price;
      var image = e.target.dataset.pic;

        
      if (cart[curpid] != undefined) {
        cart[curpid].quantity = cart[curpid].quantity + 1;
        
      } else {
        cart[curpid] = {quantity: 1, name : name, price: price, image: image};
      }

      localStorage.setItem("cart", JSON.stringify(cart));
      loadData(cart)
      loadnavbartotal()
    })

$('.tocartbtn').on('click', function(e){
    var qty = $('#tocartqty').val()

    var curpid = e.target.dataset.pid;
      var name = e.target.dataset.name;
      var price = e.target.dataset.price;
      var image = e.target.dataset.pic;

        
      if (cart[curpid] != undefined) {
        cart[curpid].quantity = cart[curpid].quantity + Number(qty);
        
      } else {
        cart[curpid] = {quantity: 1, name : name, price: price, image: image};
      }

      localStorage.setItem("cart", JSON.stringify(cart));
      loadData(cart)
      loadnavbartotal()

})


// Adding product to wishlist
            
    $('.addtowishlist').on('click', function(e){
        var productid = e.target.dataset.wishlistprodid
        
        $.ajax({url: '/wishlist',
     
     data: {'wishlistid': productid},

     success: (data)=>{
        
        if(data.added == true){
        $(this).attr('class', "fa fa-check addtowishlist") 
            
            $('.total_in_wishlist').html(data.wishlistcount) 
        }
    },

     error: () =>{
         console.log('Unsuccessful')
     }
     
     })

     })




    $('#tableforcart').on('click', '.closebtn', function (e) {

        cart = JSON.parse(localStorage.getItem('cart'))
        for (const key in cart) {
            if(key == e.target.dataset.pid){
                delete cart[key]         
            }
        }
        
        localStorage.setItem("cart", JSON.stringify(cart));
        loadData(cart)

        loadcartitems()
        
    })
   
    })



function loadcartitems(){

    var tablebody = document.getElementById('cartitemsbody')
    var cartsubtotal =  document.getElementById('cartsubtotal')
    var items = JSON.parse(localStorage.getItem('cart'))
    
    var elem = 0.0

    if (tablebody != null){
        tablebody.innerHTML = ''
    
   Object.keys(items).forEach(cartitem =>{
    elem = elem + parseFloat(items[cartitem].price * items[cartitem].quantity)
    var row = document.createElement('tr')
    row.innerHTML = `
                        <td class="shoping__cart__item">
                            <img src="${items[cartitem].image}" width="100" height="100" alt="">
                            <h5>${ items[cartitem].name }</h5>
                        </td>
                        <td class="shoping__cart__price">
                            $${parseFloat(items[cartitem].price).toFixed(2)}
                        </td>
                        <td class="shoping__cart__quantity">
                            <div class="quantity">
                                <div class="pro-qty">
                                    <input type="number" class="itemqty" data-pid="${cartitem}" min=1 value="${items[cartitem].quantity}">
                                </div>
                            </div>
                        </td>
                        <td class="shoping__cart__total">
                            $ ${parseFloat(items[cartitem].price * items[cartitem].quantity).toFixed(2)}
                        </td>
                        <td class="shoping__cart__item__close">
                            <span class="icon_close closebtn" data-pid="${cartitem}"></span>
                        </td>
                    `
                    if(tablebody != null){
                        tablebody.appendChild(row)
                    }
                    console.log('Total amount: ', elem)
   })

}
   
   
   if(cartsubtotal != null){
   document.getElementById('cartsubtotal').innerHTML =   `$${parseFloat(elem).toFixed(2)}`
   document.getElementById('carttotal').innerHTML = `$${parseFloat(elem).toFixed(2)}`
}
   document.getElementById('topcarttotal1').innerHTML =   `$${parseFloat(elem).toFixed(2)}`
   document.getElementById('topcarttotal2').innerHTML = `$${parseFloat(elem).toFixed(2)}`
   

}

function loadData(cart){
    localStorage.setItem("cart", JSON.stringify(cart));

    document.getElementById('shopbag1').innerHTML = Object.keys(cart).length 
    document.getElementById('shopbag2').innerHTML = Object.keys(cart).length 
}

$('#tableforcart').on('input', '.itemqty', function (e) {
    var cart = JSON.parse(localStorage.getItem('cart'))
    var curpid = e.target.dataset.pid;
  
    if (cart[curpid] != undefined) {
        cart[curpid].quantity = Number(e.target.value) 
        localStorage.setItem("cart", JSON.stringify(cart));

        loadcartitems()
        loadData(cart)
    }  

})

loadnavbartotal()

function loadnavbartotal(){
    var items = JSON.parse(localStorage.getItem('cart'))
    
    var elem = 0.0
Object.keys(items).forEach(cartitem =>{
    elem = elem + parseFloat(items[cartitem].price * items[cartitem].quantity)
})
document.getElementById('topcarttotal1').innerHTML =   `$${parseFloat(elem).toFixed(2)}`
document.getElementById('topcarttotal2').innerHTML = `$${parseFloat(elem).toFixed(2)}`


}
    


$('#tableforwishlist').on('click', '.removewish', function (e) {

    var wid = e.target.dataset.wishid
      
    $.ajax(
        {url: '/wishlist',
     
    data: {'wid': wid},

    success: (data)=>{
        $('#tableforwishlist').html('')
    
       for (const item of data.wishlists) {
       
        console.log(item)
        var newrow = `<tr>
        <td class="shoping__cart__item">
            <img src="${item['product__image']}" width=100 height=100 alt="${item['product__name']}">
            <h5>${item['product__name']}</h5>
        </td>
        <td class="shoping__cart__price">
            $${item['product__price']}
        </td>

        <td class="shoping__cart__price">
            In stock
        </td>

        <td class="shoping__product">
            <a href="{% url 'detail' ${item['id']} %}" ><button class="btn-secondary btn-lg">View Product</button></a>
        </td>
      
        <td class="shoping__cart__item__close">
            <span class="icon_close removewish" data-wishid="${item['id']}"></span>
        </td>
    </tr>`

        $('#tableforwishlist').append(newrow)
       }

    
    //    $('#tableforwishlist').append('Berekete')
      
    //  $('.total_in_wishlist').html(data.wishlistcount) 
     
   }
    
})})