import "./HorizontalAlignment.mjs";
document.querySelectorAll("#Ratings > form").forEach(Element => Element.addEventListener("click", function(Event){
  this.querySelector("button").click();
  window.location.reload();
}));