#!/usr/bin/env python3
"""Fase A — Korpus sintetis ENIP (build_corpus.py)

20 naskah: 10 injeksi error (2/gaya) + 6 kontrol bersih (twin) +
4 semi-formal. Injeksi 10 kategori PUEBI (E1-E10), deterministik,
seed 42, 15-25 error/naskah, offset di teks FINAL (hasil injeksi).

Usage:
  python3 build_corpus.py --build
  python3 build_corpus.py --review [id]     # diff clean vs injected
"""
import argparse
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT
RAW = CORPUS / "raw"
TEXTS = CORPUS / "texts"
SEED = 42
DIGIT = {"satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
         "tujuh": 7, "delapan": 8, "sembilan": 9}

AUDIENCE = {
    "aca": "akademisi",
    "jur": "pembaca umum (media massa)",
    "sas": "pembaca sastra",
    "pop": "pembaca umum (populer-edukatif)",
    "per": "pembaca umum (opini/advokasi)",
    "sf": "pembaca media sosial/blog",
}

# ---------------------------------------------------------------- templates

TEMPLATES = {
    "aca": {
        "titles": [
            "Korelasi Kebiasaan Membaca dan Prestasi Akademik",
            "Replikasi dalam Penelitian Ilmiah: Urgensi dan Tantangan",
        ],
        "texts": [
"""Penelitian tentang hubungan antara kebiasaan membaca dan prestasi akademik terus berkembang seiring meningkatnya minat pada literasi digital. Tiga universitas di Indonesia telah membentuk konsorsium untuk meneliti topik ini sejak tahun 2024. Namun, sebagian besar studi terdahulu, yang menggunakan sampel terbatas, masih memperlihatkan hasil yang beragam, sehingga perlu dibedah secara lebih sistematis. Tulisan ini berupaya mengkaji korelasi tersebut pada 320 siswa sekolah menengah di tiga kota besar, yaitu Jakarta, Surabaya, dan Makassar.

Metode yang digunakan adalah survei daring dengan kuesioner terstruktur yang diunggah ke *platform* survei. Data kebiasaan membaca dikumpulkan melalui instrumen yang telah diuji validitasnya, sedangkan data prestasi akademik diperoleh dari nilai rapor semester genap tahun 2026. Analisis data dilakukan menggunakan *software* statistik, dan korelasi dihitung dengan koefisien Pearson. Hasil awal menunjukkan korelasi positif yang lemah, tetapi signifikan, antara durasi membaca dan nilai rata-rata siswa. Tiga dari empat siswa mengaku membaca kurang dari satu jam per hari, dan angka tersebut menjadi bahan diskusi yang menarik bagi para peneliti.

Interpretasi hasil ini perlu dilakukan secara hati-hati. Kebiasaan membaca yang diukur masih bergantung pada laporan diri siswa, sehingga risiko bias sosial kerap kali tidak dapat dihindari. Variasi temuan mungkin disebabkan oleh perbedaan instrumen pengukuran antarstudi. Dua penelitian lain melaporkan hasil yang bertentangan, namun keduanya menggunakan kelompok usia yang berbeda. Selain itu, sampel yang digunakan hanya berasal dari sekolah perkotaan, walaupun keragaman geografis sebenarnya diperlukan untuk generalisasi. Oleh karena itu, peneliti menyarankan agar studi lanjutan menggunakan desain longitudinal dengan pengukuran objektif. Sumber data tambahan, seperti catatan perpustakaan sekolah, juga dapat memperkuat validitas temuan.

Secara teoretis, temuan ini sejalan dengan teori kognitif yang menekankan peran membaca dalam pembentukan skema pengetahuan. Membaca secara teratur, menurut teori tersebut, membuka ruang bagi pembaca untuk menghubungkan informasi baru dengan pengetahuan lama. Pada praktiknya, kemampuan ini terbukti membantu siswa memahami teks yang kompleks. Sistem evaluasi yang dipakai di sekolah pun perlu diperhatikan, karena kualitas instrumen menentukan kualitas data. Namun, perlu dicatat bahwa korelasi tidak selalu berarti sebab akibat. Keterampilan membaca yang baik justru dapat memengaruhi kebiasaan membaca, bukan sebaliknya. Penelitian selanjutnya disarankan untuk menguji arah hubungan tersebut dengan data longitudinal. Implikasi praktis dari temuan ini dapat diterapkan di perpustakaan sekolah dan di ruang kelas secara bersamaan.""",
"""Replikasi merupakan salah satu fondasi metode ilmiah yang sering kali luput dari perhatian. Peneliti baru disarankan untuk mengulang eksperimen klasik demi menguji keandalan temuan, tetapi banyak jurnal menolak naskah yang hanya berisi replikasi. Dua studi yang dikaji dalam tulisan ini memperlihatkan situasi tersebut secara jelas. Studi pertama menguji efek *deadline* pendek terhadap kinerja menulis, sedangkan studi kedua menguji pengaruh umpan balik sejawat terhadap kualitas draf.

Studi pertama melibatkan 60 mahasiswa yang dibagi menjadi dua kelompok. Kelompok pertama diberi waktu dua hari, kelompok kedua diberi waktu dua minggu. Hasilnya menunjukkan bahwa kelompok ber-*deadline* pendek menghasilkan lebih sedikit revisi, tetapi skor koherensi tidak berbeda secara signifikan. Studi kedua, yang menggunakan 45 partisipan, menemukan bahwa umpan balik sejawat meningkatkan kejelasan argumen. Namun, kedua studi sama-sama mengalami kendala praktik yang serupa, yaitu kesulitan memperoleh izin etik dalam waktu singkat. Empat dosen senior yang diwawancarai mengakui bahwa pendanaan replikasi jarang menjadi prioritas di kampus mereka.

Perluasan replikasi menghadapi tiga tantangan utama. Pertama, biaya eksperimen yang tinggi kerap menghambat peneliti di negara berkembang. Kedua, sistem insentif akademik cenderung menghargai temuan baru daripada konfirmasi. Ketiga, akses terhadap peralatan laboratorium masih terbatas di banyak kampus. Walaupun tantangan tersebut nyata, beberapa komunitas riset telah membangun *database* bersama agar data mentah dapat diakses publik. Inisiatif serupa juga didorong oleh kebijakan *open access* di berbagai institusi. Dua lembaga pendanaan di Eropa bahkan telah menetapkan kuota khusus untuk studi ulang, dan hasilnya cukup menggembirakan. Lima negara di Asia Tenggara sedang menyusun kebijakan serupa, walaupun prosesnya berjalan lambat.

Kesimpulan tulisan ini sederhana. Replikasi tidak boleh dianggap sebagai pekerjaan kelas dua, melainkan sebagai pengujian kualitas yang wajib dilakukan. Penurunan kualitas klaim ilmiah akhir-akhir ini justru sering kali disebabkan oleh kurangnya replikasi. Oleh karena itu, editor jurnal diharapkan membuka ruang yang lebih luas bagi studi replikasi. Perubahan kebijakan semacam ini dapat dimulai dari dewan redaksi di setiap kampus, kemudian diadopsi secara bertahap oleh asosiasi peneliti nasional.

Pada akhirnya, replikasi menuntut perubahan budaya, bukan sekadar aturan administratif. Empat asosiasi jurnal telah menyatakan dukungan, tetapi kebijakan di lapangan masih berjalan lambat, walaupun sosialisasi terus dilakukan di berbagai kampus. Evaluasi berkala pada tahun 2026 dapat menjadi titik awal yang konkret, karena perubahan kecil sering kali disebabkan oleh dorongan dari komunitas peneliti itu sendiri.""",
        ],
    },
    "jur": {
        "titles": [
            "Pameran Batik Nusantara Resmi Dibuka di Jakarta",
            "Kota Ramaikan Festival Kuliner dengan Dua Ratus UMKM",
        ],
        "texts": [
"""Jakarta, 14 Maret 2026 - Pameran Batik Nusantara resmi dibuka di Balai Sarbini pada Sabtu lalu. Acara ini menampilkan karya dari 120 perajin yang tersebar di tiga puluh kota. Menteri Perindustrian hadir sebagai pembicara utama, kemudian dilanjutkan dengan pemotongan pita oleh Ketua Dewan Kerajinan Daerah. Tiga stan khusus disediakan untuk perajin muda agar mereka dapat memperkenalkan karya tanpa biaya sewa.

Pameran ini diselenggarakan untuk memperkenalkan kekayaan motif batik kepada generasi muda. Menurut panitia, jumlah pengunjung hari pertama mencapai delapan ribu orang, dan angka ini melampaui target awal. Beberapa pengunjung mengaku datang sejak pagi, tetapi harus mengantre cukup lama di pintu masuk. Satu pengunjung asal Yogyakarta mengapresiasi variasi motif yang ditampilkan, walaupun ia menyayangkan harga tiket yang dirasa cukup tinggi. Panitia menyanggupi untuk mengevaluasi kebijakan tersebut pada tahun 2026. Dua direktur galeri nasional juga hadir dan berencana menjalin kerja sama dengan perajin lokal.

Di sisi lain, para perajin memanfaatkan momen ini untuk memasarkan produk secara langsung di dalam gedung. Sebagian besar stan menerima pembayaran digital, sehingga transaksi berjalan cepat di semua titik. Risiko pemalsuan motif, menurut asosiasi perajin, tetap menjadi perhatian utama. Mereka berharap pemerintah memperkuat sistem pengawasan hak kekayaan intelektual. Kepala Dinas Perindustrian menambahkan bahwa izin usaha bagi perajin kecil akan diproses lebih cepat melalui layanan *online* yang baru. Empat kota lain berencana mengadakan pameran serupa, dan jadwalnya akan diumumkan bulan depan.

Pameran akan berlangsung selama sepuluh hari dan ditutup pada 24 Maret. Pengunjung dapat menikmati *workshop* membatik setiap akhir pekan tanpa biaya tambahan. Tiga stan khusus didedikasikan untuk perajin difabel, dan dua stan lainnya menampilkan batik dari limbah tekstil. Panitia mengharapkan kegiatan ini dapat meningkatkan kualitas produk batik lokal sekaligus memperkuat ekosistem kreatif nasional. Dukungan dari pemerintah daerah dinilai penting, karena keberlanjutan acara ini sangat bergantung pada pendanaan yang solid.

Panitia juga menyiapkan area khusus untuk dialog antara perajin dan pembeli, sedangkan forum digital dibuka untuk menjaring masukan publik. Walaupun persiapan terbilang singkat, koordinasi berjalan lancar di semua lini. Empat pertemuan daring telah digelar sejak bulan lalu, dan hasil diskusinya akan dibacakan pada acara penutup. Kehadiran delegasi dari luar negeri, yang diundang melalui jalur diplomasi budaya, turut memperkaya pameran kali ini.""",
"""Surabaya, 21 Maret 2026 - Festival Kuliner Kota Pahlawan resmi dibuka di Taman Bungkul. Acara ini menghadirkan dua ratus usaha mikro, kecil, dan menengah dari berbagai daerah di Jawa Timur. Wali Kota menyebut festival ini sebagai upaya membangkitkan ekonomi warga, kemudian menandatangani kerja sama dengan operator *marketplace* daring. Tiga zona utama disiapkan panitia untuk memisahkan jenis dagangan agar pengunjung tidak bingung.

Festival ini menyediakan tiga zona utama, yaitu zona kopi, zona jajanan tradisional, dan zona makanan fermentasi. Menurut panitia, zona kopi menjadi favorit pengunjung, tetapi antrean di zona jajanan tradisional justru paling panjang. Banyak pengunjung datang bersama keluarga, dan mereka menghabiskan waktu hingga sore hari di dalam taman. Satu pedagang asal Kediri mengaku kehabisan stok pada hari kedua karena permintaan melampaui perkiraan. Ia berencana menambah pasokan pada akhir pekan, walaupun harga bahan baku sempat naik di pasar induk.

Kepala Dinas Koperasi menjelaskan bahwa festival ini merupakan bagian dari program pemulihan ekonomi daerah. Pemerintah kota menggratiskan sewa stan bagi pedagang kecil, sedangkan pedagang yang menyediakan kemasan ramah lingkungan mendapatkan insentif tambahan. Walaupun cuaca sempat diguyur hujan pada Jumat malam, panitia telah menyiapkan tenda cadangan. Dua petugas kebersihan tambahan ditempatkan di setiap zona agar suasana tetap nyaman. Pengelolaan sampah dilakukan secara terpisah, kemudian diangkut ke bank sampah terdekat. Lima komunitas kuliner juga ikut memeriahkan acara dengan demonstrasi memasak setiap sore. Sistem pemesanan *online* yang disiapkan sejak awal terbukti membantu mengurangi antrean di loket.

Festival akan berlangsung selama dua minggu. Pada hari terakhir, panitia berencana mengadakan kompetisi memasak terbuka yang diikuti oleh dua belas komunitas. Pengunjung diharapkan memanfaatkan transportasi umum, karena area parkir dibatasi untuk mengurangi kemacetan. Panitia memperkirakan total pengunjung mencapai lima puluh ribu orang, dan angka ini akan dievaluasi untuk perencanaan tahun depan. Keberhasilan festival tahun ini, menurut pengamat kuliner, sangat dipengaruhi oleh kolaborasi antara pemerintah dan pelaku usaha di lapangan.

Empat sponsor utama telah mengonfirmasi dukungan untuk edisi tahun depan, tetapi panitia menegaskan bahwa keputusan akhir tetap menunggu evaluasi. Kualitas acara, menurut mereka, jauh lebih penting daripada jumlah pengunjung. Tiga pengamat ekonomi juga menilai festival serupa dapat direplikasi di kota lain, walaupun masing-masing daerah memiliki karakteristik yang berbeda. Evaluasi menyeluruh akan dipublikasikan pada akhir tahun 2026.""",
        ],
    },
    "sas": {
        "titles": [
            "Hujan di Senja",
            "Penjual Roti di Stasiun",
        ],
        "texts": [
"""Hujan turun di senja hari, dan langit Jakarta berubah menjadi kelabu tua. Siti berdiri di bawah kanopi stasiun Manggarai sambil memeluk tas punggungnya. Ransel itu basah, tetapi ia tidak peduli. Selama dua jam ia menunggu kereta yang tak kunjung datang, kemudian ia melihat seorang ibu tua menjual nasi bungkus di ujung peron. Dua lampu peron berkedip redup, namun tidak seorang pun mempedulikannya.

Ibu tua itu tersenyum ketika Siti mendekat. "Roti ini masih hangat, Nak," katanya sambil menunjuk keranjang anyaman. Siti membeli dua buah roti, melainkan hanya memakan satu dan menyimpan satunya untuk adiknya di rumah. Adiknya sedang demam, dan pagi tadi ibunya berpesan agar Siti pulang sebelum gelap. Walaupun jarak rumah masih jauh, Siti mantap berjalan kaki ketika kereta batal berangkat. Dua orang petugas stasiun menyarankannya menunggu angkutan yang lewat di jalan raya. Siti mengangguk, tetapi hatinya tidak nyaman.

Perjalanan menembus hujan membawa Siti melewati pasar yang mulai sepi. Lampu pasar berkedip-kedip, dan bau sayur basah bercampur asap gerobak. Di depan toko jahit, ia melihat seorang pemuda menawarkan payung bekas. Siti tersenyum dan membeli satu payung, kemudian melanjutkan langkahnya di jalan yang basah. Risiko jatuh di jalan licin menghantuinya, tetapi ia tetap berjalan pelan. Gedung-gedung tua di sekitar kota kini tampak seperti siluet yang berdiri diam, seolah-olah menjadi saksi bagi langkah kecilnya. Tiga anak bermain di teras rumah, dan salah satunya melambaikan tangan ketika Siti lewat. Ia membalas dengan senyum tipis, kemudian mempercepat langkah karena hujan mulai reda. Selama perjalanan, Siti teringat pesan ibunya untuk tidak berhenti di tempat sepi. Di pintu gerbang, seorang penjaga menawarkan diri mengantar Siti ke jalan raya, tetapi Siti menolak dengan sopan. Lima menit kemudian, ia tiba di perempatan yang cukup ramai, dan angkutan kota pun melintas. Risiko kelelahan mulai terasa, namun langkahnya tetap ringan karena mengingat roti hangat untuk adiknya. Sampai di rumah, Siti mendapati adiknya tertidur pulas. Roti kedua yang ia simpan masih hangat, dan senyum mengembang di wajahnya yang lelah. Di luar, hujan akhirnya berhenti, dan lampu jalan mulai menyala satu per satu.""",
"""Setiap sore pukul lima, Pak Karta membuka lapak roti di depan pintu masuk stasiun. Roti yang ia jual dibuat oleh istrinya di dapur rumah sejak subuh. Tiga orang satpam stasiun sudah mengenalnya, dan mereka selalu menyapa ketika gerbong pertama tiba. Pak Karta tersenyum, kemudian menyusun roti di rak kayu yang sudah usang. "Roti hangat, harganya tetap," ia berteriak pelan kepada penumpang yang bergegas. Dua orang penumpang berhenti sejenak, tetapi lebih memilih kopi daripada roti.

Banyak penumpang membeli roti, tetapi tidak sedikit pula yang hanya menoleh. Pak Karta tidak pernah kehilangan akal. Ia mengganti kemasan roti dengan kertas cokelat, karena kualitas kemasan menentukan kesan pertama pembeli. Istri Pak Karta menyarankan agar ia mencoba berjualan secara *online*, tetapi Pak Karta merasa lebih nyaman bertemu pembeli langsung. Dua tahun lalu, sebuah toko besar menawarinya izin berjualan di mal, namun ia menolak. Ia lebih memilih bertahan di stasiun, dekat dengan orang-orang yang berlalu lalang setiap hari. Empat penumpang tetap setia membeli roti setiap pagi, walaupun jumlahnya berkurang di musim hujan.

Pada suatu senja, seorang gadis membeli dua roti dan membayar dengan uang lebih. "Kembaliannya simpan saja," kata gadis itu. Pak Karta mengembalikan uang dengan halus, kemudian menceritakan kisah masa mudanya ketika bekerja di pelabuhan. Gadis itu tersenyum mendengar cerita, walaupun ia harus segera mengejar kereta terakhir. Sejak hari itu, gadis tersebut mampir setiap minggu, dan mereka berbincang tentang banyak hal, mulai dari harga beras hingga rencana liburan. Tiga kali ia terlambat mengejar kereta karena terlalu asyik mendengar cerita. Beberapa pembeli menanyakan roti pisang, tetapi Pak Karta hanya tersenyum dan menunjuk rak kosong. Tiga kios di pasar sebelah kini turut memesan roti setiap pagi, sehingga pesanan bertambah sejak tahun 2025. Ia berencana meminta bantuan keponakannya di akhir pekan, walaupun istrinya lebih suka mengerjakannya sendiri. Roti Pak Karta tetap hangat, dan stasiun tetap ramai. Suatu sore, hujan turun deras, tetapi Pak Karta memilih menutup lapaknya lebih awal. Ia memikirkan istrinya yang sedang sakit, dan langkahnya berubah cepat. Ia berjanji, esok pagi, roti akan kembali dibawa ke stasiun.""",
        ],
    },
    "pop": {
        "titles": [
            "Mengapa Kita Lupa: Ilmu di Balik Memori",
            "Rahasia Kopi: Dari Biji ke Cangkir",
        ],
        "texts": [
"""Pernahkah Anda masuk ke dapur untuk mengambil sesuatu, tetapi kemudian lupa apa yang ingin diambil? Fenomena ini bukan sekadar kebetulan, melainkan bagian dari cara kerja memori manusia. Para ilmuwan menjelaskan bahwa otak kita tidak menyimpan ingatan seperti *hard disk*, melainkan merakitnya kembali setiap kali dibutuhkan. Proses ini melibatkan tiga tahap, yaitu penyandian, penyimpanan, dan pemanggilan kembali. Dua tahap pertama sering berjalan tanpa kita sadari, sedangkan tahap terakhir biasanya yang paling sering gagal.

Tahap penyandian terjadi ketika informasi baru masuk. Semakin kuat perhatian yang diberikan, semakin besar kemungkinan informasi tersebut disimpan dengan baik. Dua penelitian di Jepang menunjukkan bahwa peserta yang membagi perhatian saat belajar mengingat 40 persen lebih sedikit daripada mereka yang fokus. Walaupun hasil tersebut hanya mengukur satu kondisi, dampaknya nyata dalam kehidupan sehari-hari. Empat dari lima orang dewasa mengaku pernah lupa nama orang yang baru dikenalnya pada situasi seperti ini. Lima percobaan tambahan di universitas lain menghasilkan pola yang serupa, maka para ahli mulai menyusun panduan praktis.

Selain perhatian, emosi juga memengaruhi ingatan. Peristiwa yang memicu emosi kuat, seperti pernikahan atau kecelakaan, biasanya diingat lebih jelas. Namun, ingatan emosional juga rentan terhadap distorsi, sehingga kesaksian saksi mata sering kali tidak akurat. Para ahli menyarankan agar orang mencatat informasi penting, karena menulis ulang membantu memperkuat jejak memori. Risiko salah ingat pun dapat ditekan dengan cara ini. Pada praktiknya, kebiasaan mencatat kecil ini terbukti efektif bagi siswa dan pekerja profesional. Sistem pengingat berbasis aplikasi kini juga banyak digunakan, walaupun efektivitasnya masih diperdebatkan.

Ada juga fenomena yang disebut efek *tip-of-the-tongue*, yaitu kondisi ketika informasi terasa di ujung lidah, tetapi tidak berhasil diucapkan. Kondisi ini meningkat seiring bertambahnya usia, namun tidak selalu menandakan gangguan serius. Otak yang sehat tetap melewati proses ini sebagai bagian dari *refresh* alami. Yang penting adalah memahami cara kerja memori, sehingga kita tidak mudah panik ketika lupa. Sistem latihan mengingat, seperti pengulangan berjarak, dapat membantu menjaga daya ingat. Dengan pendekatan yang sederhana, kualitas hidup kita pun meningkat, dan kebiasaan lupa yang membuat frustrasi dapat dikelola dengan lebih tenang.""",
"""Kopi bukan sekadar minuman, melainkan ritual pagi bagi jutaan orang. Di balik secangkir kopi, terdapat perjalanan panjang yang dimulai dari biji di pegunungan. Proses pengolahan kopi terbagi menjadi beberapa tahap, dan setiap tahap menentukan rasa akhir di cangkir. Petani memetik buah kopi pada waktu tertentu, kemudian menjemurnya di bawah sinar matahari. Dua tahap penting dalam pengolahan adalah fermentasi dan pengeringan, yang keduanya memengaruhi profil rasa. Tiga metode pengolahan kini populer, yaitu metode basah, kering, dan semi-basah.

Metode penyeduhan juga berperan besar. Alat seperti *pour-over* dan *french press* menghasilkan tekstur yang berbeda, sedangkan espreso mengekstraksi rasa dengan tekanan tinggi. Para barista terlatih memperhatikan suhu air, karena air yang terlalu panas dapat menghasilkan rasa pahit. Walaupun terlihat sederhana, proses ini menuntut konsistensi dalam setiap langkah. Risiko utama dalam penyeduhan adalah ekstraksi berlebih, yang membuat kopi terasa membakar. Satu kesalahan kecil, seperti gilingan yang terlalu halus, dapat mengubah segalanya. Empat barista yang diwawancarai sepakat bahwa kontrol suhu adalah kunci utama.

Banyak orang bertanya mengapa harga kopi bervariasi. Jawabannya terletak pada kualitas biji, ketinggian kebun, dan metode panen. Kopi yang dipetik dengan tangan, misalnya, dihargai lebih tinggi karena hanya buah matang yang dikumpulkan. Sistem perdagangan langsung antara petani dan roaster juga mulai populer, karena memberikan keuntungan yang lebih adil. Kebiasaan ini didorong oleh konsumen yang peduli pada keberlanjutan. Empat dari lima konsumen di kota besar, menurut survei, bersedia membayar lebih untuk kopi yang ramah lingkungan. Dua koperasi di Sumatera bahkan telah mengekspor kopi organik ke pasar Eropa.

Pada akhirnya, menikmati kopi adalah soal keseimbangan. Tidak ada metode terbaik secara mutlak, melainkan metode yang paling sesuai dengan selera masing-masing. Setiap cangkir membawa cerita yang dimulai dari kebun hingga meja kita. Dengan memahami prosesnya, kita dapat menghargai setiap tegukan, dan mungkin, mencoba variasi baru dengan keberanian yang lebih besar. Panduan ini diharapkan dapat membantu pembaca memulai perjalanan kopi mereka sendiri, baik di rumah maupun di kedai favorit.

Ada kabar baik bagi pecinta kopi lokal. Dua kedai kecil di Semarang bahkan memulai kelas seduh terbuka, sehingga konsumen dapat belajar langsung dari barista. Kualitas biji lokal pun meningkat seiring permintaan yang stabil, walaupun tantangan cuaca masih sering kali muncul di musim hujan. Evaluasi pada tahun 2026 akan memperlihatkan tren yang lebih jelas, dan harganya pun akan lebih mudah diprediksi.""",
        ],
    },
    "per": {
        "titles": [
            "Literasi Keuangan Bukan Pilihan, Melainkan Kebutuhan",
            "Urbanisasi dan Masa Depan Desa",
        ],
        "texts": [
"""Literasi keuangan sering kali dianggap sebagai urusan orang dewasa yang bekerja di kantor. Pandangan ini keliru, melainkan justru berbahaya bagi generasi muda. Lima tahun terakhir memperlihatkan peningkatan utang konsumtif di kalangan mahasiswa, dan kebiasaan ini diprediksi akan berlanjut. Data dari lembaga survei menunjukkan bahwa delapan dari sepuluh mahasiswa tidak memahami perbedaan antara kebutuhan dan keinginan. Kondisi ini diperparah oleh kemudahan akses pinjaman *online* yang menawarkan proses cepat tanpa penjelasan risiko. Dua kasus gagal bayar di kampus besar bahkan berujung pada masalah hukum yang berkepanjangan.

Kita perlu menanamkan literasi keuangan sejak dini, mulai dari bangku sekolah dasar. Pendidikan ini tidak harus rumit. Sekolah dapat mengajarkan cara membedakan kebutuhan, menyusun anggaran sederhana, dan menabung secara teratur. Walaupun mata pelajaran tersebut belum menjadi kurikulum wajib, beberapa daerah telah memulai program percontohan. Empat sekolah di Yogyakarta, misalnya, berhasil menurunkan angka jajan berlebihan melalui program kantin sehat. Bukti sederhana ini menunjukkan bahwa perubahan mungkin dilakukan tanpa menunggu kebijakan besar. Tiga perguruan tinggi juga telah menambahkan mata kuliah literasi keuangan, dan jumlah pendaftarnya meningkat setiap semester.

Pemerintah juga memiliki peran yang tidak kalah penting. Regulasi perlu diperkuat, sedangkan pengawasan terhadap penawaran kredit bermasalah harus diperketat. Izin bagi platform pinjaman hendaknya disertai kewajiban edukasi kepada pengguna. Lebih jauh lagi, bank sentral dapat mendorong bank milik negara untuk membuka kelas keuangan gratis di setiap cabang. Biaya program semacam ini relatif kecil dibandingkan kerugian akibat utang macet. Pada tahun 2026, evaluasi menyeluruh atas kebijakan ini diharapkan dapat dimulai. Sistem pelaporan konsumen yang transparan juga perlu dibangun agar praktik penagihan yang agresif dapat ditindak. Jangan biarkan generasi muda belajar dari kesalahan yang seharusnya dapat dicegah. Investasi di bidang literasi keuangan merupakan investasi yang paling menguntungkan, karena dampaknya dirasakan selama puluhan tahun. Dibutuhkan keberanian untuk memulai, tetapi hasilnya akan dinikmati oleh semua pihak, termasuk anak cucu kita nanti.

Komitmen ini tidak dapat dibebankan kepada satu lembaga saja, melainkan harus menjadi gerakan bersama. Dua kampanye literasi telah berjalan di sekolah dan di kantor, tetapi cakupannya masih terbatas di kota besar. Evaluasi pada tahun 2026 akan menunjukkan sejauh mana perubahan yang dicapai, dan hasilnya dapat menjadi dasar bagi kebijakan berikutnya. Kerja sama antarlembaga pun menjadi syarat utama, karena kesenjangan literasi sering kali disebabkan oleh minimnya koordinasi.""",
"""Setiap tahun, ribuan pemuda desa memilih pindah ke kota besar. Mereka berharap memperoleh pekerjaan yang lebih baik, tetapi sering kali berakhir di sektor informal dengan upah minim. Dua faktor utama mendorong urbanisasi ini, yaitu keterbatasan lapangan kerja di desa dan janji kemudahan hidup di kota. Walaupun angka migrasi terus meningkat, pemerintah tampak belum memiliki strategi terpadu. Satu konsekuensi yang nyata adalah menurunnya jumlah tenaga kerja muda di sektor pertanian. Akibatnya, banyak lahan produktif terbengkalai, dan ketahanan pangan perlahan mulai terancam.

Solusi jangka panjang harus menyentuh akar masalah, bukan sekadar membatasi perpindahan penduduk. Pemerintah daerah perlu membangun ekosistem ekonomi baru di desa, seperti pengolahan hasil tani dan wisata edukasi. Dukungan berupa izin usaha yang sederhana dan akses modal tanpa agunan akan membantu warga memulai usaha kecil. Menurut para pengamat, pendekatan ini terbukti berhasil di beberapa kabupaten di Sulawesi. Lima desa di Kabupaten Gowa kini memiliki koperasi pengolahan kakao yang memasok produk ke kota besar, sehingga pemuda setempat tidak perlu pergi merantau. Tiga desa lainnya sedang mengembangkan wisata edukasi, dan hasilnya mulai terlihat dalam dua tahun terakhir.

Kita juga perlu mengubah cara pandang terhadap desa. Desa bukan tempat singgah, melainkan ruang untuk bertumbuh. Fasilitas pendidikan dan kesehatan yang setara menjadi kunci agar keluarga muda tetap tinggal. Investasi di desa sering kali dianggap memakan biaya besar, tetapi biaya tersebut jauh lebih kecil daripada biaya sosial urbanisasi. Walaupun prosesnya bertahap, perubahan kecil di tingkat desa dapat merambat menjadi perubahan besar. Sudah saatnya desa mendapat perhatian yang seimbang dengan kota. Dukungan *online* bagi pemasaran produk desa dapat menjadi pintu masuk yang efektif, sedangkan pembinaan wirausaha dilakukan secara langsung di lapangan. Dengan komitmen bersama, masa depan desa tidak harus suram, dan masa depan kota pun menjadi lebih tertata. Perubahan ini tidak akan terjadi dalam semalam, tetapi setiap langkah kecil bernilai besar.

Desa dan kota sejatinya saling membutuhkan, tetapi kebijakan yang ada sering kali memperlakukan keduanya secara terpisah. Dua lembaga penelitian merekomendasikan perencanaan bersama, dan usulan tersebut layak dipertimbangkan pada tahun 2026. Kemauan politik menjadi penentu utama, karena kebijakan yang baik sering kali gagal disebabkan oleh lemahnya pelaksanaan. Dengan dialog yang terbuka antara desa dan kota, harapan itu bukan sekadar mimpi.""",
        ],
    },
}

SEMIFORMAL = [
("Catatan Pindah Kota: Laporan Pertama",
"""Jadi, akhirnya gue resmi pindah ke Bandung minggu lalu. Jujur, gue kira bakal langsung adaptasi, tapi ternyata banyak hal kecil yang bikin kaget. Pertama, soal transportasi. Gue sempat bingung, tapi untungnya temen kosan ngajarin pakai aplikasi transportasi umum. Kedua, soal hujan. Bandung hujannya tiba-tiba, jadi sekarang gue selalu bawa payung compact di tas.

Buat yang lagi berencana pindah, gue kasih beberapa catatan penting. Sempatkan riset dulu soal area domisili, terutama dekat gak sama tempat kerja. Cek juga soal biaya hidup, karena harga makanan di pusat kota lebih mahal dari perkiraan. Awal bulan pasti banyak pengeluaran, jadi siapin dana cadangan. Gue sempat salah hitung, dan akhirnya nabung dulu buat sebulan pertama. FYI, tempat kos yang bagus biasanya cepet keisi, jadi booking lebih awal.

Hari ini gue dapet pengalaman seru. Ada tetangga kos yang ngajak makan bareng, dan ternyata kita satu angkatan SMA, walaupun beda jurusan. Kecil dunia ini, kan? Setelah itu gue juga nemu kafe kecil favorit yang harganya bersahabat. Tempatnya nyaman buat baca atau kerja laptop. Gue jadi mikir, pindah kota itu ternyata lebih tentang orang-orangnya daripada gedung-gedungnya. Semoga minggu depan makin banyak cerita bagus. Nanti gue update lagi.

Oh iya, satu hal yang gue pelajari: jangan bandingin prosesmu dengan orang lain. Temen kos gue udah nemu kerja seminggu setelah pindah, sedangkan gue masih santai cari kenyamanan dulu. Walaupun sempat insecure, gue sadar setiap orang punya ritme masing-masing. Dua minggu ke depan gue rencanain buat eksplor rute baru ke kantor, sekalian cari spot makan siang yang enak tapi ramah dompet. Kalau kalian punya tips biar cepat adaptasi, langsung aja tulis di kolom komentar. Siapa tahu bisa jadi catatan buat yang baru pindah juga. Gue tunggu cerita kalian. Besok rencananya gue ke kota lama buat urus dokumen, dan semoga nggak macet kayak kemarin. Banyak cerita baru yang nunggu ditulis, tapi cukup dulu buat hari ini. Daaah!""",),
("Belajar Bahasa di Era Streaming",
"""Dulu orang bilang belajar bahasa butuh ke luar negeri atau les mahal. Sekarang, dengan *streaming* dan medsos, semua bisa belajar dari kamar sendiri. Gue sendiri mulai serius belajar Jepang setahun lalu, dan kemajuan paling pesat justru dari nonton anime tanpa subtitle. Awalnya gue cuma nangkep kata "hai" dan "arigatou", tapi sekarang udah bisa ngikutin alur drama dengan lumayan paham.

Tips pertama, konsisten tapi santai. Target jangan muluk-muluk, cukup 15 menit sehari. Kedua, pilih konten yang seru dulu. Kalau suka musik, hafalin lirik; kalau suka masak, tonton video masak dengan subs. Kuncinya bikin belajar terasa seperti main, bukan tugas. Gue juga rajin nyatet kosakata baru di notes HP, terus dibaca pas lagi antre atau di kendaraan umum. Lima kata sehari pun cukup, asal rutin.

Hambatan terbesar? Disiplin dan malu ngomong. Gue atasi yang kedua dengan latihan ngomong sendiri di kamar. Kedengeran aneh, tapi efektif banget buat melancarkan lidah. Kalau ada temen, bisa bikin sesi ngobrol seminggu sekali. Sekarang gue lagi nyari partner bahasa lewat aplikasi *language exchange*. Seru sih, tapi lokasi waktu beda kadang bikin susah ketemu. Semoga minggu depan dapet jadwal yang pas. Yang penting, jangan berhenti walau progres terasa lambat.

Satu hal lagi, jangan ragu cari komunitas. Biasanya ada grup belajar yang ketemuan mingguan, dan suasana belajarnya beda banget pas bareng orang lain. Tiga temen belajar gue sekarang ketemu rutin tiap Sabtu pagi, dan kita saling koreksi cara ngomong. Walaupun progres tiap orang beda, suasananya selalu bikin semangat. Gue juga mulai rajin cek kamus digital buat kata-kata yang sulit, terus nyimpen contoh kalimatnya di catatan khusus. Empat bulan lagi target gue bisa ngobrol santai tanpa mikir panjang. Kalau kalian pengen coba, mulai aja dari konten favorit. Siapa tahu ketagihan, kan? Nanti kalau udah dapet progress yang signifikan, gue bakal bikin video singkat buat dokumentasi. Doain aja, ya. Minggu depan gue juga mau coba bikin jadwal belajar yang lebih rapi, biar progresnya makin keliatan.""",),
("Weekend Produktif Tanpa Stres",
"""Weekend sering jadi teka-teki antara malas-malasan dan pengen produktif. Menurut pengalaman gue, jawabannya bukan soal jumlah kegiatan, tapi soal pilihan yang pas. Gue sekarang bikin aturan sederhana: satu kegiatan menyenangkan, satu kegiatan bermanfaat, dan satu waktu untuk benar-benar istirahat. Tiga hal itu cukup, nggak perlu lebih.

Sabtu kemarin contohnya. Pagi gue jemur bantal dan cek perlengkapan dapur, karena kata ibu, anomali bau apek itu tanda bantal perlu dijemur. Setelah itu gue ke pasar, beli sayur untuk masak seminggu. Sesampainya di rumah, gue masak tumisan sederhana sambil dengar podcast. Sorenya, gue jalan santai ke taman dekat kos sambil bawa buku. Itu udah terasa lengkap, tanpa perlu rencana mewah.

Nah, biar konsep ini jalan, penting juga buat nggak maksa diri. Kalau badan capek banget, jadwal bisa ditukar: istirahat dulu, sisanya belakangan. Gue selalu ingetin diri, produktif itu soal melakukan hal yang menenangkan hati, bukan cuma ngisi jam. Dua kategori lain mungkin bergeser ke hari kerja, dan itu nggak apa-apa. Minggu depan gue mau coba bikin roti sederhana. Kalau berhasil, resepnya gue tulis di sini.

Oh iya, jangan lupa kadang-kadang nggak melakukan apa-apa juga perlu. Menurut gue, istirahat itu bukan kemalasan, melainkan bagian dari ritme hidup. Banyak orang salah paham soal produktivitas, padahal otak butuh jeda biar bisa mikir jernih. Dua minggu lalu gue sempet burnout, dan pelajarannya mahal: gue nggak bisa maksa terus. Sekarang gue jadwalkan tidur lebih awal, dan hasilnya jauh lebih baik. Walaupun masih suka overplanning, gue makin sadar buat stop di tengah jalan kalau badan udah ngasih sinyal. Temen-temen juga bilang wajah gue lebih fresh. Itu bonus yang nggak bisa dibeli. Semoga catatan kecil ini membantu kalian yang lagi ngerasa lelah. Minggu depan gue mau coba bikin roti lagi, versi lebih besar. Kalau berhasil, gue bagi resepnya. Ditunggu, ya. Sekarang gue mau fokus nyelesain buku yang udah lama setengah dibaca.""",),
("Review: Drama Korea yang Bikin Mikir",
"""Drama Korea terbaru yang gue tonton minggu ini judulnya boleh dibilang bikin mikir. Alurnya sederhana: empat sahabat yang dulu satu SMA, sekarang dipertemukan lagi karena proyek komunitas. Kedengarannya biasa, tapi pembahasannya dalam banget soal persahabatan yang berubah karena kesuksesan yang beda. Satu karakter yang sukses bisnis tapi kesepian, satu lagi yang bahagia tapi dianggap tidak berprestasi. Komentar-komentar di medsos juga rame membahas dua karakter ini.

Kenapa gue suka? Karena konfliknya realistis. Nggak ada penjahat besar, yang ada cuma salah paham kecil yang menumpuk. Adegan favorit gue ada di episode lima, ketika dua sahabat akhirnya ngobrol dari hati ke hati di stasiun. Adegan itu nggak dramatis, justru itu yang bikin haru. Visualnya juga bagus banget, dan musik latarnya pas. Semua elemen kecil itu nyatu jadi cerita yang hangat.

Tapi, jujur, ada beberapa bagian yang agak lambat. Tiga episode terakhir seharusnya bisa dirangkum jadi dua. Untungnya, karakter pendukungnya kuat, jadi tetap seru buat ditonton sampai akhir. Kalau kalian suka drama yang tenang dengan dialog yang bermakna, gue rekomendasikan banget. Sekalian belajar, adegan-adegannya bisa dipakai buat latihan listening. Skor gue delapan dari sepuluh. Nanti kalau ada drama bagus lagi, gue review lagi.

Satu catatan penutup: jangan lupa tonton versi subtitle dulu kalau masih baru, biar nggak ketinggalan alur. Setelah itu, coba lagi tanpa subtitle, dan rasakan bedanya. Tiga temen gue udah coba metode ini, dan dua di antaranya bilang kemampuan dengerinnya naik lumayan. Walaupun tiap orang beda, metode ini layak dicoba. Gue juga sempet nemu teori menarik di *forum* diskusi soal pengaruh drama pada pola pikir, dan itu bikin gue makin penasaran. Oh iya, drama ini juga ngajarin gue soal kesabaran: kadang hal terbaik justru datang di akhir cerita. Kayak hidup aja, ya. Kalau nanti gue nemu konten menarik lain, gue tulis di sini lagi. Sekarang gue udah siap mulai menonton ulang dari episode pertama, biar menemukan detail yang sempat terlewat. Sampai jumpa di catatan berikutnya!""",),
]

# ---------------------------------------------------------------- injection


def make_candidates(text):
    cands = []  # (start, end, cat, wrong, right)

    def add(m, cat, wrong, right, g=0):
        s = m.start(g) if g else m.start()
        e = m.end(g) if g else m.end()
        cands.append((s, e, cat, wrong, right))

    for m in re.finditer(r",\s*(tetapi|melainkan|sedangkan)\b", text):
        add(m, "E1", " " + m.group(1), m.group(0))
    for m in re.finditer(r"\bdi\s+(rumah|sekolah|pasar|kota|desa|kantor|perpustakaan|kampus|klinik|pabrik|jalan|lapangan|taman|stasiun|pintu)\b", text):
        add(m, "E2", "di" + m.group(1), m.group(0))
    for m in re.finditer(r"\bdi(baca|tulis|buka|jual|terapkan|bangun|kelola|anggap|bahas|pakai|ukur|lihat|miliki|ambil|jemur|dapat|tangani)\b", text):
        add(m, "E2", "di " + m.group(1), m.group(0))
    for m in re.finditer(r"\b(walaupun|meskipun|adapun)\b", text):
        w = m.group(0)
        wrong = "walau pun" if w == "walaupun" else "meski pun" if w == "meskipun" else "ada pun"
        add(m, "E3", wrong, w)
    SER = {"praktik": "praktek", "risiko": "resiko", "apotek": "apotik",
           "izin": "ijin", "analisis": "analisa", "kualitas": "kwalitas",
           "sistem": "sistim", "teknologi": "tehnologi", "hierarki": "hirarki",
           "jadwal": "jadual", "aktivitas": "aktifitas", "jumat": "jum'at"}
    for m in re.finditer(r"\b(" + "|".join(SER) + r")\b", text):
        w = m.group(1)
        add(m, "E4", SER[w], w)
    for m in re.finditer(r"\bmerupakan\b", text):
        add(m, "E5", "adalah merupakan", "merupakan")
    for m in re.finditer(r"\bagar\b", text):
        add(m, "E5", "agar supaya", "agar")
    for m in re.finditer(r"\bpara\s+([a-z]+)\b", text):
        add(m, "E5", "banyak para " + m.group(1), m.group(0))
    for m in re.finditer(r"(?:^|[.!?…] )([Tt]iga|[Dd]ua|[Ee]mpat|[Ll]ima|[Ee]nam|[Tt]ujuh|[Dd]elapan|[Ss]embilan|[Ss]atu)(?= )", text):
        add(m, "E6", str(DIGIT[m.group(1).lower()]), m.group(1), g=1)
    for m in re.finditer(r"\b((?:19|20)\d{2})\b", text):
        y = m.group(1)
        add(m, "E7", y[0] + "." + y[1:], y)
    for m in re.finditer(r"(?:^|[.!?…] )([A-Z][a-z]+)(?= )", text):
        add(m, "E8", m.group(1).lower(), m.group(1), g=1)
    for m in re.finditer(r"\*([a-zA-Z][a-zA-Z-]*)\*", text):
        add(m, "E9", m.group(1), m.group(0))
    for m in re.finditer(r"\bdisebabkan oleh\b", text):
        add(m, "E10", "disebabkan karena", "disebabkan oleh")
    return cands


def inject(text, rng, min_errors=15, max_errors=25):
    cands = make_candidates(text)
    rng.shuffle(cands)
    per_cat = {}
    chosen = []
    covered = []
    for c in cands:
        cat = c[2]
        if per_cat.get(cat, 0) >= 6:
            continue
        if any(not (c[1] <= s or c[0] >= e) for s, e in covered):
            continue
        chosen.append(c)
        covered.append((c[0], c[1]))
        per_cat[cat] = per_cat.get(cat, 0) + 1
        if len(chosen) >= max_errors:
            break
    if len(chosen) < min_errors:
        raise RuntimeError(f"kandidat tidak cukup: {len(chosen)} < {min_errors}")
    chosen.sort(key=lambda c: c[0])
    out = text
    delta = 0
    errors = []
    for start, end, cat, wrong, right in chosen:
        final_pos = start + delta
        out = out[:start] + wrong + out[end:]
        delta += len(wrong) - (end - start)
        errors.append({"cat": cat, "offset": final_pos, "wrong": wrong, "right": right})
    return out, errors

# ---------------------------------------------------------------- build


def build():
    RAW.mkdir(parents=True, exist_ok=True)
    TEXTS.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    meta = []
    per_cat_total = Counter()

    for style, tpl in TEMPLATES.items():
        for i, (title, clean) in enumerate(zip(tpl["titles"], tpl["texts"]), start=1):
            injected, errors = inject(clean, rng)
            for e in errors:
                per_cat_total[e["cat"]] += 1
            tid = f"{style}_{i:02d}"
            (TEXTS / f"{tid}.txt").write_text(injected, encoding="utf-8")
            (RAW / f"{tid}_clean.txt").write_text(clean, encoding="utf-8")
            meta.append({"id": tid, "title": title, "style": style,
                         "audience": AUDIENCE[style], "words": len(clean.split()),
                         "variant": "injected", "clean_twin": None,
                         "injected_errors": errors})
            print(f"  {tid}: {len(errors)} error di-injeksi "
                  f"({len(clean.split())} kata bersih) -> {len(injected.split())} kata final")

    twins = [("aca", 0, "aca_01", "aca_03"), ("aca", 1, "aca_02", "aca_04"),
             ("jur", 0, "jur_01", "jur_03"), ("sas", 0, "sas_01", "sas_03"),
             ("pop", 0, "pop_01", "pop_03"), ("per", 0, "per_01", "per_03")]
    for style, ti, injected_id, tid in twins:
        clean = TEMPLATES[style]["texts"][ti]
        (TEXTS / f"{tid}.txt").write_text(clean, encoding="utf-8")
        (RAW / f"{tid}_clean.txt").write_text(clean, encoding="utf-8")
        meta.append({"id": tid, "title": TEMPLATES[style]["titles"][ti],
                     "style": style, "audience": AUDIENCE[style],
                     "words": len(clean.split()), "variant": "clean",
                     "clean_twin": injected_id, "injected_errors": []})
        print(f"  {tid}: KONTROL bersih ({len(clean.split())} kata), twin={injected_id}")
        for m in meta:
            if m["id"] == injected_id:
                m["clean_twin"] = tid

    for i, (title, clean) in enumerate(SEMIFORMAL, start=1):
        tid = f"sf_{i:02d}"
        (TEXTS / f"{tid}.txt").write_text(clean, encoding="utf-8")
        (RAW / f"{tid}_clean.txt").write_text(clean, encoding="utf-8")
        meta.append({"id": tid, "title": title, "style": "sf",
                     "audience": AUDIENCE["sf"], "words": len(clean.split()),
                     "variant": "semiformal", "clean_twin": None,
                     "injected_errors": []})
        print(f"  {tid}: SEMI-FORMAL ({len(clean.split())} kata)")

    (CORPUS / "metadata.json").write_text(
        json.dumps({"seed": SEED, "n": len(meta),
                    "error_catalog": "E1..E10 (lihat PLAN.md)",
                    "corpus": meta}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(f"\nTotal: {len(meta)} naskah -> corpus/texts/")
    print("Sebaran kategori injeksi (seluruh set):",
          ", ".join(f"{k}={v}" for k, v in sorted(per_cat_total.items())))
    low = [(m["id"], len(m["injected_errors"])) for m in meta
           if m["variant"] == "injected" and len(m["injected_errors"]) < 15]
    if low:
        print("PERINGATAN injeksi rendah:", low)
    out_of_range = [m["id"] for m in meta if not (300 <= m["words"] <= 600)]
    if out_of_range:
        print("PERINGATAN di luar 300-600 kata:", out_of_range)


def review(sel):
    meta = json.loads((CORPUS / "metadata.json").read_text(encoding="utf-8"))
    for m in meta["corpus"]:
        if sel and m["id"] != sel:
            continue
        if m["variant"] != "injected":
            continue
        print(f"\n=== {m['id']} ({m['style']}) — {len(m['injected_errors'])} error ===")
        for e in m["injected_errors"]:
            print(f"  [{e['cat']}] @{e['offset']}  '{e['right']}' -> '{e['wrong']}'")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--review", nargs="?", const="", default=None)
    a = ap.parse_args()
    if a.build:
        build()
    if a.review is not None:
        review(a.review or None)


if __name__ == "__main__":
    main()