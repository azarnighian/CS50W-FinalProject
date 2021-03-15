document.addEventListener('DOMContentLoaded', function () {
    noMatch();     
    
    document.querySelector('.filters-bar').addEventListener('click', () => filters_bar());
});

function noMatch() {
    const text = document.getElementById("no_match");

    if (text) {
        document.querySelector('.cards-container').style.justifyContent = 'center';
        document.querySelector('.sidebar-and-cards-container').style.cssText = "flex-direction:column; width:100%;"                
        document.querySelector('.sidebar-container').style.cssText = "display:none; align-self:center; text-align:center; margin-left: 0;"        
        document.querySelector('.filters-bar').style.cssText = "display:block; width:20%; padding:15px;"       
        document.getElementById('filters_header').style.display = 'none';        
        document.querySelector('input[name = location]').style.textAlign = 'center';
        document.querySelector('input[name = radius]').style.textAlign = 'center';
        document.querySelector('select').style.textAlign = 'center';
        document.querySelector('input[type = submit]').style.cssText = "width:60%; align-self:center; text-align:center;"        
    }
}

function filters_bar() {
    if (document.querySelector('.sidebar-container').style.display === 'none') {
        document.querySelector('.sidebar-container').style.display = 'block';
        document.querySelector('.sidebar-and-cards-container').style.width = '100%';
        document.querySelector('.cards-container').style.display = 'none';
    }
    else {
        document.querySelector('.sidebar-container').style.display = 'none';
        document.querySelector('.cards-container').style.display = 'flex';
    }
}