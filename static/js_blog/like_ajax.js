function like(id, slug) {
    var element = document.getElementById('like')
    var count = document.getElementById('count')

    $.get(`/blog/like/${id}/${slug}`).then(response =>{
        if (response['response'] === 'liked'){
            element.className = 'fa fa-heart px-2'
            count.innerText = Number(count.innerText) + 1
        }else{
            element.className = 'fa fa-heart-o px-2'
            count.innerText = Number(count.innerText) - 1
        }
    })
}

// function like(id, slug) {
//     var element = document.getElementById('like');
//     var count = document.getElementById('count');
//
//     $.ajax({
//         url: `/blog/like/${id}/${slug}/`,
//         type: 'GET',
//         success: function(response) {
//             if (response.response === 'liked') {
//                 element.className = 'fa fa-heart px-2';
//                 count.innerText = response.count;
//             } else {
//                 element.className = 'fa fa-heart-o px-2';
//                 count.innerText = response.count;
//             }
//         },
//         error: function(xhr, status, error) {
//             console.error("Error:", error);
//         }
//     });
// }
