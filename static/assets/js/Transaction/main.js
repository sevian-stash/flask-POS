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
	let trx_id = doc.querySelector('#IV_ID').value;
	let trx_sidenav_amount = doc.querySelector('#IV_AMOUNT');
	let trx_sidenav_qty = doc.querySelector('#IV_QTY');

	$('.transaction-item').on('hidden.bs.collapse', function(event) {
		const item = event.currentTarget;

		/* Color Switch & Add to Cart */
		let item_id = item.parentElement.id;
		let item_name = item.parentElement.dataset.name;
		let item_price = item.parentElement.dataset.price;
		let item_qty = item.querySelector('[name="transaction-item-amount"]').value;
		let item_class = item.classList;

		trx.IV_AMOUNT = 0;
		trx.IV_QTY = 0;

		if(item_qty > 0) { /* Item Addition */
			cart[item_id] = {IV_ITEMNAME:item_name, IV_ITEMPRICE:item_price, IV_ITEMQTY:item_qty};
			item_class.add('text-light');
			item_class.add('bg-primary');
		} 
		else { /* Item Removal */
			cart.hasOwnProperty(item_id) && delete cart[item_id];
			item_class.remove('text-light');
			item_class.remove('bg-primary');
		}

		/* Total Trx Amount */
		for (const item in cart) {
			trx.IV_AMOUNT += (cart[item].IV_ITEMPRICE * cart[item].IV_ITEMQTY);
		}

		trx.item = cart;
		trx.IV_QTY = Object.keys(cart).length;
		localStorage.setItem(trx_id, JSON.stringify(trx));

		trx_sidenav_amount.value = (trx.IV_AMOUNT).toLocaleString('en-US');
		trx_sidenav_qty.value = trx.IV_QTY;
	});


	/* Checkout Modal Logic */
	$('#transaction-modal').on('show.bs.modal', function(event) {
		console.log('MODAL OPENED');
		
		const modal = event.currentTarget;
		const table = document.querySelector('#form-detail-table')
		const tbody = table.querySelector('tbody')

		let local_trx = JSON.parse(localStorage.getItem(trx_id));
		let local_trx_qty = local_trx.IV_QTY;
		let local_trx_keys = Object.keys(local_trx.item);

		local_trx_keys.forEach((key,idx)=>{
			tbody.innerHTML += `
				<tr>
					<td><input type="text" name="IV_ID_${idx}" class="form-control form-control-sm border-0 bg-transparent text-light" value="${key}" readonly> </td>
					<td><input type="text" name="IV_NAME_${idx}" class="form-control form-control-sm border-0 bg-transparent text-light" value="${local_trx.item[key].IV_ITEMNAME}" readonly> </td>
					<td><input type="text" name="IV_QTY_${idx}" class="form-control form-control-sm border-0 bg-transparent text-light text-right" value="${local_trx.item[key].IV_ITEMQTY}" readonly> </td>
					<td><input type="text" name="IV_SELLPRICE_${idx}" class="form-control form-control-sm border-0 bg-transparent text-light text-right" value="${parseInt(local_trx.item[key].IV_ITEMPRICE).toLocaleString('en-US')}" readonly> </td>
				</tr>
			`
		})

		const new_item = `<td></td>`


	})

	/* Display Open Transaction List */


})();