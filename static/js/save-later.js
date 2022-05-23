// // form.js
// const formId = "book"; // ID of the form
// const url = location.href; //  href for the page
// const formIdentifier = `${url} ${formId}`; // Identifier used to identify the form
// const saveButton = document.querySelector("#save"); // select save button
// const alertBox = document.querySelector(".alert"); // select alert display div
// let form = document.querySelector(`#${formId}`); // select form
// let formElements = form.elements; // get the elements in the form

// /**
//  * This function gets the values in the form
//  * and returns them as an object with the
//  * [formIdentifier] as the object key
//  * @returns {Object}
//  */
// const getFormData = () => {
//   let data = { [formIdentifier]: {} };
//   for (const element of formElements) {
//     if (element.name.length > 0) {
//       data[formIdentifier][element.name] = element.value;
//     }
//   }
//   return data;
// };

// saveButton.onclick = event => {
//   event.preventDefault();
//   data = getFormData();
//   localStorage.setItem(formIdentifier, JSON.stringify(data[formIdentifier]));
//   const message = "Form draft has been saved!";
//   displayAlert(message);
// };

// /**
//  * This function displays a message
//  * on the page for 1 second
//  *
//  * @param {String} message
//  */
// const displayAlert = message => {
//   alertBox.innerText = message;
//   alertBox.style.display = "block";
//   setTimeout(function() {
//     alertBox.style.display = "none";
//   }, 1000);
// };

// /**
//  * This function populates the form
//  * with data from localStorage
//  *
//  */
// function populateForm() {
//   if (localStorage.key(formIdentifier)) {
//     const savedData = JSON.parse(localStorage.getItem(formIdentifier)); // get and parse the saved data from localStorage
//     no_forms = savedData['form-TOTAL_FORMS']
//     document.getElementById('location').value=savedData['location']
    
     
//     for(count = 0; count < parseInt(no_forms); count++){
//         document.getElementById('add').click();}
    
//     for (const element of formElements) {
//       if (element.name in savedData) {
//             element.value = savedData[element.name];
//       }}
//       for(count = 0; count < parseInt(no_forms); count++){
//         filter_date(count);
//         $(`input[name="form-${count}-date"]`).on("change", function(){filter_time(count);})
//       }

//   const message = "Form has been refilled with saved data!";
//     displayAlert(message);
//   }
// };



function filter_date(num){
    $.ajax({
        type:'GET',
        url: 'appointment/ajax/filter-dates',
        data:{
            'clinic' : $("#location").val(),

        },
        dataType:'json',

        success:function(response){

            jQuery(function(){
            // function change(data){enableDays=data}
            
            $(`#form-${num}-date`).datepicker('destroy');
            var datesEnabled = response.dates;
            console.log(datesEnabled);

            $(`#form-${num}-date`).datepicker({
              format:'mm/dd/yyyy',    beforeShowDay: function (date) {
            var allDates = `${date.getDate()}`.padStart(2, 0) + '-' + `${date.getMonth() + 1}`.padStart(2,0)+ '-' + date.getFullYear();
            if(datesEnabled.indexOf(allDates) != -1)
            return true;
            else
            return false;
            }
            });          
        })
        }
    })
}

 function filter_time(num){
        $.ajax({
            type:'GET',
            url:'appointment/ajax/filter-times',
            data:{
                'clinic':$('#location').val(),
                'date':$(`input[name="form-${num}-date"]`).val(),
            },
            dataType:'json',
            success:function(response){
                var select = document.getElementById(`form-${num}-time`);
                select.innerHTML = null;
                for (var i=0;i<response.times.length;i++){
                    var option = document.createElement('option');
                    option.value = response.times[i]['id'];
                    option.innerHTML = response.times[i]['time'];
                    select.appendChild(option)
                }
            }
    })
 }
                

$(document).on('click','#add', function(){

    var total = document.getElementById('id_form-TOTAL_FORMS')

    var form = document.querySelectorAll('.bookrow');
    var container = document.getElementById('form');
    var before = document.getElementById('add');
    var formnum = form.length-1
    var newform = form[0].cloneNode(true)
    var select = newform.childNodes[7].childNodes[5].options
    while (select.length > 0){select.remove(0);}

    let formRegex = RegExp(`form-(\\d){1}-`,'g')
    formnum++
    newform.innerHTML = newform.innerHTML.replace(formRegex, `form-${formnum}-`);

    container.insertBefore(newform,before);


    total.setAttribute('value', `${formnum+1}`);
    filter_date(formnum);

    $(`input[name="form-${formnum}-date"]`).on("change", function(){filter_time(formnum);})
    })


function delete_form(e){
    console.log('k')
    var total = document.getElementById('id_form-TOTAL_FORMS');
    if (window.confirm('Are you sure you want to delete?')){
    m=e.parentNode.parentNode
    m.remove()
    total.setAttribute('value', `${formnum-1}`)
    }
    }

        $('#location').on("change", function (){
            $('#repeater').load(window.location.href +" #repeater", function(){
                filter_date(0);
                $('input[name="form-0-date"]').on("change", function(){filter_time(0);})
            });
            })

// populateForm() // populate the form when the document is loaded
