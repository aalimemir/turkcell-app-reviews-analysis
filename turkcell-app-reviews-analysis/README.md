📊 Turkcell App Reviews: Sentiment Analysis \& Insights



Bu proje, Turkcell mobil uygulamasının Google Play Store üzerindeki binlerce kullanıcı yorumunu analiz etmek ve makine öğrenmesi teknikleriyle anlamlı içgörüler çıkarmak amacıyla geliştirilmiştir. Proje, ham verinin temizlenmesinden model eğitimine ve interaktif bir dashboard sunumuna kadar tüm veri bilimi süreçlerini kapsar.



&nbsp;📈 Proje Kapsamı ve Analitik Yaklaşım



Proje süresince veri üzerinde şu temel işlemler gerçekleştirilmiştir:


Analiz sürecinde **Lojistik Regresyon (Logistic Regression)** algoritması kullanılmış ve modelin duygu durumlarını tahminlemede **%89 doğruluk (accuracy)** oranına ulaştığı gözlemlenmiştir.

\* NLP \& Veri Temizleme: Ham yorumlar üzerindeki noktalama işaretleri, etkisiz kelimeler (stop-words) ve gereksiz karakterler temizlenerek metin madenciliğine hazır hale getirilmiştir.

\* Sentiment Analysis (Duygu Analizi): Eğitilen Makine Öğrenmesi modeli sayesinde kullanıcı yorumları "Olumlu" veya "Olumsuz" olarak sınıflandırılmaktadır.

\* Etki Analizi: Uygulama puanındaki değişimler zaman serisi olarak incelenmiş, kullanıcıların en çok hangi konularda (hız, fatura, giriş vb.) sorun yaşadığı veya memnun kaldığı tespit edilmiştir.

\* Jupyter Notebook Süreci: Tüm veri ön işleme, keşifsel veri analizi (EDA) ve model eğitim adımları `turkcelldata.ipynb` dosyasında şeffaf bir şekilde dökümante edilmiştir.



&nbsp;🛠️ Teknik Araçlar ve Kütüphaneler



\- Dil: Python

\- Veri Analizi: Pandas, NumPy

\- Görselleştirme: Matplotlib, Seaborn

\- Makine Öğrenmesi: Scikit-learn (Model \& Vectorizer)

\- Arayüz: Streamlit



&nbsp;🚀 Kurulum ve Kullanım



1\. Kütüphaneleri Yükleyin

Bash

pip install -r requirements.txt

2. Dashboard'u Çalıştırın

Analiz sonuçlarını ve duygu analizi tahminleme ekranını görüntülemek için:



Bash

streamlit run app.py



📂 Dosya Yapısı

app.py: Streamlit dashboard arayüzü.



turkcelldata.ipynb: Veri analizi ve model eğitim aşamaları.



turkcell\_model.pkl \& vectorizer.pkl: Eğitilmiş makine öğrenmesi ağırlıkları.



turkcell\_yorumlar\_final.csv: Temizlenmiş ve analize hazır veri setidir.



⭐ Bu proje, kullanıcı geri bildirimlerini veri odaklı bir yaklaşımla analiz ederek müşteri deneyimini anlamlandırmak için tasarlanmıştır.




