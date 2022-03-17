const MapElement = document.querySelector("#Map");
const Map = new google.maps.Map(MapElement, {
  "zoom": 12.,
  "center": new google.maps.LatLng(MapElement.dataset.lat, MapElement.dataset.lng),
  "mapTypeId": google.maps.MapTypeId.ROADMAP
});

let SelectedMarker = null;

google.maps.event.addListener(Map, "click", function(Event){
  //Set values of hidden latitude and longitude inputs to make form submission easier
  document.querySelector("#HiddenLatitudeInput").value = Event.latLng.lat();
  document.querySelector("#HiddenLongitudeInput").value = Event.latLng.lng();

  //Hide map selection hint
  document.querySelector("#MapTitleExplanation").style.opacity = "0";

  //Create a marker if it doesn't exist and move it to the clicked location
  SelectedMarker ??= new google.maps.Marker({
    "map": Map,
    "title": "Place location"
  });
  SelectedMarker.setPosition(Event.latLng);
});

const SelectTypeMenu = document.querySelector("#SelectTypeMenu");
const SelectedType = document.querySelector("#SelectTypeMenu > div > div:first-child");
const HiddenInput = document.querySelector("#HiddenPlaceTypeInput");

SelectTypeMenu.addEventListener("click", function(Event){
  const Type = Event.target.dataset.type;
  if(Type === undefined) return;
  SelectedType.innerText = Event.target.innerText;
  HiddenInput.value = Type;
});
