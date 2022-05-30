# PyQT Crud Uygulaması

Python PyQT ile kodladığım basit bir crud uygulamasıdır. Veritabanı işlemleri için 'SqlAlchemy' kullanılmıştır.


Projedeki gerekli kütüphaneleri kurmamız için gerekli koddur.

## Proje Hakkında

Proje veritabanı dili olarak MySQL kullanmaktadır. Veritabanı işlemlerini ORM yapısında yapar.

## Kurulum aşaması
```
pip install -r requirements.txt 
```

Bu komut ile beraber projeye gerekli olan kütüphaneler kurulur.

```
mysql -u 'username' -p
```

şeklinde cli ortamından veritabanı bağlantımızı yapalım ve veritabanımızı oluşturalım;

```
CREATE DATABASE 'dbname'
```

Sonrasında .env.example dosyasının adını .env yapalım ve içerisindeki ortam değişkenleri değerlerini kendimize göre düzenleyelim.

```
python main.py
```

şeklinde programımızı artık çalıştırabiliriz.

## Önizleme

![Onizleme](https://i.ibb.co/mzzX03k/Ekran-Goruntusu-20220530-194035.png "Onizleme")