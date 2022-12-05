# =[Modules dan Packages]========================

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from joblib import load
import json

# =[Variabel Global]=============================

app = Flask(__name__, static_url_path='/static')
model = None

# =[Routing]=====================================

# [Routing untuk Halaman Utama atau Home]


@app.route("/")
def beranda():
    return render_template('index.html')

@app.route("/rekomendasi")
def rekomendasi():
    return render_template('rekomendasi.html')
# [Routing untuk API]


@app.route("/api/deteksi", methods=['POST'])
def apiDeteksi():
     # Nilai default untuk variabel input atau features (X) ke model
    input_nilai_matematika = 0
    input_jurusan_sekolah = 1
    input_minat1 = 1
    input_minat2 = 0
    input_karir1 = 1
    input_karir2 = 0

    if request.method == 'POST':
        # Set nilai untuk variabel input atau features (X) berdasarkan input dari pengguna
        input_nilai_matematika = float(request.form['nilai_matematika'])
        input_jurusan_sekolah = int(request.form['jurusan'])
        input_minat1 = int(request.form['minat1'])
        input_minat2 = int(request.form['minat2'])
        input_karir1 = int(request.form['karir1'])
        input_karir2 = int(request.form['karir2'])

        # Prediksi kelas atau spesies bunga iris berdasarkan data pengukuran yg diberikan pengguna
        df_test = pd.DataFrame(data={
            "Nilai Matematika": [input_nilai_matematika],
            "Jurusan saat Sekolah": [input_jurusan_sekolah],
            "Minat1": [input_minat1],
            "Minat2": [input_minat2],
            "Karir1": [input_karir1],
            "Karir2": [input_karir2],
        })

        hasil_rekomendasi = model.predict(df_test[0:1])[0]

        # Set Path untuk gambar hasil rekomendasi
        if hasil_rekomendasi == 1:
            jurusan_rekomendasi = 'Teknik Informatika'
        elif hasil_rekomendasi == 2:
            jurusan_rekomendasi = 'Manajemen Informatika'
        elif hasil_rekomendasi == 3:
            jurusan_rekomendasi = 'Sistem Informasi'
        elif hasil_rekomendasi == 4:
            jurusan_rekomendasi = 'Teknik Komputer'
        else:
            jurusan_rekomendasi = 'Teknologi Informasi'

        class NpEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, np.integer):
                    return int(obj)
                if isinstance(obj, np.floating):
                    return float(obj)
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                return super(NpEncoder, self).default(obj)
        
        hasil_rekomendasi = json.dumps(hasil_rekomendasi, cls=NpEncoder)
        jurusan_rekomendasi = json.dumps(jurusan_rekomendasi, cls=NpEncoder)

        # Return hasil rekomendasi dengan format JSON
        return jsonify({
            "rekomendasi": hasil_rekomendasi,
            "jurusan_rekomendasi": jurusan_rekomendasi
        })

# =[Main]========================================


if __name__ == '__main__':

     # Load model yang telah ditraining
    model = load('dt_model.model')

    # Run Flask di localhost
    app.run(host="localhost", port=5000, debug=True)