$(document).ready(function(){
  
    // -[Animasi Scroll]---------------------------
    
    $(".navbar a, footer a[href='#home']").on('click', function(event) {
      if (this.hash !== "") {
        event.preventDefault();
        var hash = this.hash;
        $('html, body').animate({
          scrollTop: $(hash).offset().top
        }, 900, function(){
          window.location.hash = hash;
        });
      } 
    });
    
    $(window).scroll(function() {
      $(".slideanim").each(function(){
        var pos = $(this).offset().top;
        var winTop = $(window).scrollTop();
          if (pos < winTop + 600) {
            $(this).addClass("slide");
          }
      });
    });
  
    
    // -[Prediksi Model]---------------------------
    
    // Fungsi untuk memanggil API ketika tombol prediksi ditekan
    $("#proses_submit").click(function(e) {
      e.preventDefault();
      
      // Set data jurusan dari input pengguna
      var input_nilai_matematika = $("#nilai_matematika").val(); 
      var input_jurusan_sekolah  = $("#jurusan").val(); 
      var input_minat1 = $("#minat_1").val(); 
      var input_minat2  = $("#minat_2").val(); 
      var input_karir1 = $("#prospek_karir1").val(); 
      var input_karir2  = $("#prospek_karir2").val();
  
      // Panggil API dengan timeout 1 detik (1000 ms)
      setTimeout(function() {
        try {
              $.ajax({
                url  : "/api/deteksi",
                type : "POST",
                data : {"nilai_matematika" : input_nilai_matematika,
                        "jurusan"  : input_jurusan_sekolah,
                        "minat1" : input_minat1,
                        "minat2"  : input_minat2,
                        "karir1" : input_karir1,
                        "karir2"  : input_karir2,
                       },
                success:function(res){
                  // Ambil hasil prediksi jurusan dari API
                  res_data_rekomendasi   = res['jurusan_rekomendasi']
                  
                  
                  // Tampilkan hasil rekomendasi ke halaman web
                  generate_rekomendasi(res_data_rekomendasi); 
                }
              });
          }
          catch(e) {
              // Jika gagal memanggil API, tampilkan error di console
              console.log("Gagal !");
              console.log(e);
          } 
      }, 1000)
      
    })
      
    // Fungsi untuk menampilkan hasil prediksi model
    function generate_rekomendasi(res_data_rekomendasi) {
      var str="";
      str += "<h3>Hasil Rekomendasi </h3>";
      str += "<br>";
      str += "<h3>Berdasarkan rekomendasi, maka jurusan yang direkomendasikan yaitu : </h3>";
      str += "<h3>" + res_data_rekomendasi + "</h3>";
      $("#hasil_rekomendasi").html(str);
    }  
    
  })
    
  