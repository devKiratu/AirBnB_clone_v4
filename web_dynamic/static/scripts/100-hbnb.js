$(document).ready(function () {
  // Check API status
  $.get('http://0.0.0.0:5001/api/v1/status/', function (res) {
    if (res.status === 'OK') {
      $('#api_status').addClass('available');
    } else {
      $('#api_status').removeClass('available');
    }
  });

  // Get all places
  $.ajax({
    type: 'POST',
    url: 'http://0.0.0.0:5001/api/v1/places_search/',
    contentType: 'application/json',
    data: '{}',
    dataType: 'json',
    success: fetchPlaces
  });

  $('input:checkbox:checked').prop('checked', false);

  const amenities = {};

  // Get selected amenities
  $('li.amenity input:checkbox').on('click', function () {
    if ($(this).prop('checked') === true) {
      amenities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else if ($(this).attr('data-id') in amenities) {
      delete amenities[$(this).attr('data-id')];
    }

    if (Object.values(amenities).length > 0) {
      $('div.amenities h4').text(Object.values(amenities).join(', '));
    } else {
      $('div.amenities h4').html('&nbsp;');
    }
  });

  const states = {};
  $('li.state input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      states[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete states[$(this).attr('data-id')];
    }
    const locations = Object.assign({}, states, cities);
    if (Object.values(locations).length === 0) {
      $('.locations h4').html('&nbsp;');
    } else {
      $('.locations h4').text(Object.values(locations).join(', '));
    }
  });

  const cities = {};
  $('li.city input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      cities[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete cities[$(this).attr('data-id')];
    }
    const locations = Object.assign({}, states, cities);
    if (Object.values(locations).length === 0) {
      $('.locations H4').html('&nbsp;');
    } else {
      $('.locations H4').text(Object.values(locations).join(', '));
    }
  });

  // Filter places by amenities
  $('button').on('click', function () {
    $.ajax({
      type: 'POST',
      url: 'http://0.0.0.0:5001/api/v1/places_search/',
      contentType: 'application/json',
      data: JSON.stringify({
        amenities: Object.keys(amenities),
        states: Object.keys(states),
        cities: Object.keys(cities)
      }),
      dataType: 'json',
      success: fetchPlaces
    });
  });
});

function fetchPlaces (data) {
  $('section.places').empty();
  $('section.places').append(data.map(place => {
    return `<article>
              <div class="title_box">
                <h2>${place.name}</h2>
                <div class="price_by_night">
                  $${place.price_by_night}
                </div>
              </div>
              <div class="information">
                <div class="max_guest">
                  ${place.max_guest} Guests
                </div>
                <div class="number_rooms">
                  ${place.number_rooms} Bedrooms
                </div>
                <div class="number_bathrooms">
                  ${place.number_bathrooms} Bathrooms
                </div>
              </div>
              <div class="user">
                <b>Owner:</b> firstName lastName
              </div>
              <div class="description">
                ${place.description}
              </div>
            </article>`;
  }));
}
