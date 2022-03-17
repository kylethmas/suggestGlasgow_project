void function ApplyCorrectAlignment(){
  self.requestAnimationFrame(ApplyCorrectAlignment);
  for(const ItemsWrapper of document.querySelectorAll(".ItemsWrapper")){
    //This checks for the visually horizontal overflow
    const IsOverflowing = ItemsWrapper.clientHeight < ItemsWrapper.scrollHeight;
    //This is required because "center" overflows the content in both directions,
    //and you can only have positive scroll values.
    ItemsWrapper.style.justifyContent = IsOverflowing ? "flex-start" : "center";
  }
}();
