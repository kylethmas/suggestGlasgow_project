function* ChangeText(){
    const SelectTypeMenu = document.querySelector("#SelectTypeMenu");
    const AnimatedItem = SelectTypeMenu.querySelector(":scope > div > div:first-child");
    const Options = [...SelectTypeMenu.querySelectorAll(":scope > div > div:not(:first-child)")].map(Element => Element.innerText);
    let CurrentIndex = 0;
    while(true){
        const CurrentString = Options[(CurrentIndex++) % Options.length];
        let NewString = AnimatedItem.innerText;
        for(let i = 0; i < CurrentString.length; ++i){
            NewString += CurrentString[i];
            AnimatedItem.innerText = NewString; //This is needed because html elements can't have trailing spaces
            yield Math.random() * 150. + 150.;
        }
        yield 1500.;
        for(let i = 0; i < CurrentString.length; ++i){
            NewString = NewString.slice(0, -1);
            AnimatedItem.innerText = NewString;
            yield 80.;
        }
        yield 600.;
    }
}

const ChangeTextGen = ChangeText();
void function Animate(){
    window.setTimeout(Animate, ChangeTextGen.next().value);
}();

SelectTypeMenu.addEventListener("click", function(Event){
    const Type = Event.target.dataset.type;
    if(Type === undefined) return;
    document.querySelector("#id_place_type").value = Event.target.innerText;
    document.querySelector("#SubmitButton").click(); //Submit form
});