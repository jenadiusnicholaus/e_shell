// get csrf token
function getToken(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getToken('csrftoken')

/*Generate the cart */
function getCookie(name){
    //split cookie string and get all individual  name =value in an array
    const cookieArray = document.cookie.split(';');
    //looping throughout the array present in browser cookie
    for(let i =0 ; i < cookieArray.length; i++){
        const cookiePair = cookieArray[i].split('=');

        /*Removing White space at the beginning of the cookie name
        * and comapere it with the given string */
        if(name === cookiePair[0].trim()){
        //    Decode the cookie value and return
            return decodeURIComponent(cookiePair[1]);
        }
    }
    // return null if not found
    return null
}

let cart = JSON.parse(getCookie('cart'));
// don't change to  ===
if(cart == undefined){
    cart = {};
    console.log('cart was created');
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path/';
}




// Update the cart
const updateBtns = document.getElementsByClassName('update-cart');
const user = '{{request.user.is_authenticated|yesno:"true,false"}}';

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
        const productId = this.dataset.product;
        const action = this.dataset.action;
        console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

        //  if the user is Anonymous Users
		if (user){
			addCookieItem(productId, action)
          //  if the user is not Anonymous Users
		}else{
			  updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

		var url = '/update_item/'

		fetch(url, {
			method:'POST',
			headers:{
				'Content-Type':'application/json',
				'X-CSRFToken':csrftoken,
			},
			body:JSON.stringify({'productId':productId, 'action':action})
		})
		.then((response) => {
		   return response.json();
		})
		.then((data) => {
		    location.reload()
		});
}




function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action === 'add'){
		if (cart[productId] === undefined){
  		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action === 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

	location.reload()
}


