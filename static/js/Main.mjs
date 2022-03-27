const MapElement = $("#Map")[0];
const Map = new google.maps.Map(MapElement, {
  "zoom": 12.,
  "center": new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng),
  "mapTypeId": google.maps.MapTypeId.ROADMAP
});

let SelectedMarker = null;

google.maps.event.addListener(Map, "click", function(Event){
  //Set values of hidden latitude and longitude inputs to make form submission easier
  $("#id_latitude")[0].value = Event.latLng.lat();
  $("#id_longitude")[0].value = Event.latLng.lng();

  //Hide map selection hint
  $("#MapTitleExplanation")[0].style.opacity = "0";

  //Create a marker if it doesn't exist and move it to the clicked location
  SelectedMarker ??= new google.maps.Marker({
    "map": Map,
    "title": "Place location"
  });
  SelectedMarker.setPosition(Event.latLng);
});

const SelectTypeMenu = $("#SelectTypeMenu")[0];
const SelectedType = $("#SelectTypeMenu > div > div:first-child")[0];
const HiddenInput = $("#HiddenPlaceTypeInput")[0];

$(SelectTypeMenu).click(function(Event){
  const Type = Event.target.dataset.type;
  if(Type === undefined) return;
  SelectedType.innerText = Event.target.innerText;
  HiddenInput.value = Type;
});
$("#id_place_image").change(function(Event){
	document.querySelector("#output").src = URL.createObjectURL(Event.target.files[0]);
});