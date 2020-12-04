$(document).on('click', '#btn-analyze', function(){
  $("#div_result").addClass("d-none")
  // get compose rule values
  let to_lower_case = $("#cb_lower").is(':checked')
  let strip_punctuation = $('#cb_strip_punctuation').is(':checked')
  let uniform_numbers = $("#cb_uniform").is(':checked')
  let strip_words = $("#cb_strip_words").is(':checked')
  let strip_multi_space = $("#cb_strip_spaces").is(':checked')
  let replace_whitespace = $("#cb_replace_whitespace").is(':checked')

  let t_words = $('#t_words').val()
  let s_truth = $('#ta_truth').val()
  let s_hypo = $('#ta_hypothesis').val()

  let data = {
    to_lower_case,
    strip_punctuation,
    uniform_numbers,
    strip_words,
    strip_multi_space,
    replace_whitespace,
    t_words,
    s_truth,
    s_hypo
  }

  $.ajax({
    type: 'post',
    url: '/analyze',
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    traditional: true,
    success: function (data) {
      $("#div_result").removeClass("d-none")
      if (typeof data === 'object'){
        $('#wer').text((data.wer * 100).toFixed(2))
        $('#mer').text((data.mer * 100).toFixed(2))
        $('#wil').text((data.wil * 100).toFixed(2))
        console.log("inserting part")
      }
    }
  });
})
