if (!sessionStorage.adModal) {
    setTimeout(function() {
        $('#admodal').find('.item').first().addClass('active');
        $('#admodal').modal({
            backdrop: 'static',
            keyboard: false
        });
    }, 3000);
    $('#adCarousel').carousel({
      interval: 4000,
      cycle: true
    });
    
    $("#buttonSuccess").click(function(e){
        e.preventDefault();
        var url = $(this).attr("href");
        var win = window.open(url, '_blank');
        $('#admodal').modal('hide');
    })
    sessionStorage.adModal = 1;}

    $(document).ready(function(){
        $('.start-btn').click(function(){
          $('.modal-box').toggleClass("show-modal");
          $('.start-btn').toggleClass("show-modal");
        });
        $('.fa-times').click(function(){
          $('.modal-box').toggleClass("show-modal");
          $('.start-btn').toggleClass("show-modal");
        });
      });