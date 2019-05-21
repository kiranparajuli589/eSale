
$("#item-area1").find(".itemlist").select2();
$("#item-area2").find(".itemlist").select2();
$("#item-area3").find(".itemlist").select2();


// $(document).on('click', 'input[type=button]', function () {
//
//     // $('.itemlist').select2().remove();
//     if ($('.itemlist').data('select2')) {
//        $('.itemlist').select2('destroy');
//      }
//     let noOfDivs = $('.item-area').length;
//     let $clonedDiv = $('#item-area').clone(true);
//     $clonedDiv.find('span').remove();
//     // $clonedDiv.find(".itemlist").select2({
//     //     allowClear: true
//     // });
//     $clonedDiv.attr('id', 'item-area' + noOfDivs);
//     $clonedDiv.insertBefore("#tool-placeholder");
//     $('#itemlist').select2({
//         allowClear: true
//     })
// });