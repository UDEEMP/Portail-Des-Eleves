$(function() {
	var geocoder = new google.maps.Geocoder();

	var parisBounds = new google.maps.LatLngBounds(
		new google.maps.LatLng(48.682902,2.052917),
		new google.maps.LatLng(49.003746,2.646179));
	var addrInput = document.getElementById('addressinput');

	var autocomplete = new google.maps.places.Autocomplete(addrInput);
	//autocomplete.setBounds(parisBounds);

	google.maps.event.addListener(autocomplete, 'place_changed', function() {
		$('.pac-container').addClass('.chzn-container .chzn-drop .chzn-results');
	});

	$('#editform').submit(function(e) {
		e.preventDefault();
		var noError = true;
		var address = $('input[name="ville"]').val();		
		geocoder.geocode({ 'address': address },
			function(results, status) {
				if (status == google.maps.GeocoderStatus.OK) {
					$('input[name="ville"]').val(results[0].formatted_address);
					$('input[name="latitude"]').val(results[0].geometry.location.lat());
					$('input[name="longitude"]').val(results[0].geometry.location.lng());
				} else {
					noError = false;
					//alert('Error in geocoding');
				}
				var data = $('#editform').serialize();
				$.post('/people/edit/', data, function(res) {
					/*
					if (res == 'OK') {
						alert("OK")
					}
					else {
						alert(res);
					}*/
				});
				 setTimeout(function () {
       			window.location.href = "/accounts/profile"; //will redirect to your blog page (an ex: blog.html)
    			}, 500);
				//window.location = "/accounts/profile"
			}
		);
	});
});
