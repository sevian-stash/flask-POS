/* JS For Transaction Item */

/* Immediate Activation Function */
(function () {
	console.log('Trans JS');

	const doc = document;


	/* Prevent Collapsible from Collapsing on Input */
	doc.querySelectorAll('.collapse').forEach(function (item) {
		item.onclick = (event) => event.stopPropagation();
	});

	/* Local Cart Logic */
	let cart = {};
	let trx = {};
	let trx_id = doc.querySelector('#transaction-sidenav-id').value;
	let trx_sidenav_amount = doc.querySelector('#transaction-sidenav-amount');
	let trx_sidenav_qty = doc.querySelector('#transaction-sidenav-qty');

	$('.transaction-item').on('hidden.bs.collapse', function(event) {
		const item = event.currentTarget;

		/* Color Switch & Add to Cart */
		let item_id = item.parentElement.id;
		let item_name = item.parentElement.dataset.name;
		let item_price = item.parentElement.dataset.price;
		let item_qty = item.querySelector('[name="transaction-item-amount"]').value;
		let item_class = item.classList;

		trx.total_amount = 0;
		trx.total_qty = 0;

		if(item_qty > 0) { /* Item Addition */
			cart[item_id] = {name:item_name, price:item_price, qty:item_qty};
			item_class.add('text-dark');
			item_class.add('bg-primary');
		} 
		else { /* Item Removal */
			cart.hasOwnProperty(item_id) && delete cart[item_id];
			item_class.remove('text-dark');
			item_class.remove('bg-primary');
		}

		/* Total Trx Amount */
		for (const item in cart) {
			trx.total_amount += (cart[item].price * cart[item].qty);
		}

		trx.item = cart;
		trx.total_qty = Object.keys(cart).length;
		localStorage.setItem(trx_id, JSON.stringify(trx));

		trx_sidenav_amount.value = (trx.total_amount).toLocaleString('en-US');
		trx_sidenav_qty.value = `${trx.total_qty} item(s)`;
	});


	/* Checkout Modal Logic */
	$('#transaction-modal').on('show.bs.modal', function(event) {
		console.log('MODAL OPENED');
		
		const modal = event.currentTarget;

		let local_trx = JSON.parse(localStorage.getItem(trx_id));
		let local_trx_qty = local_trx.total_qty;
		let local_trx_keys = Object.keys(local_trx);

		// local_trx_keys.forEach((item, index)=>{
			
		// });

		// for (let item in local_trx.item) {
		// 	let new_item_row = doc.createElement('div').classList.add('row');
		// 	new_item_row;

		// 	console.log(item);
		// }

		const new_item = `
				      <div class="card-body p-0 col-3">
				        <p class="card-text font-weight-bold mb-1">- ${'DESCRIPTION'}</p>
				        <p class="card-text">(${'QTY'}x) Rp.${'PRICE'}</p>
				      </div>`


	})

	/* Display Open Transaction List */


})();