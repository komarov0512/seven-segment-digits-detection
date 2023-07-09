# Recognizing digits with OpenCV and Python 
## Программа для распознавания цифр с изображения тонометра

### P.S На данный момент программа реализованна конкретно для текущего изображения

Изначально была попытка воспользоваться PyTesseract, но он не подошел т.к. шрифтов с цифрами похожими на мои не было.

В итоге за идею была взята статья https://pyimagesearch.com/2017/02/13/recognizing-digits-with-opencv-and-python/

Мое входное изображение:
![alt text](https://github.com/komarov0512/seven-segment-digits-detection/blob/main/Программа/photo.jpg)

А также входное изображение в статье:
![alt text](https://b2633864.smushcdn.com/2633864/wp-content/uploads/2017/02/example.jpg?lossy=1&strip=1&webp=1)

Видно, что изображения отличаются и поэтому пришлось изменять алгоритм подготовки изображения для дальнейшего распознования.

Т.к. тень, свет, блики, качесво фотографии очень сильно влияют на мой алгоритм, то реализовать распознование для любого изображения не получилось.

Дальнейшая цель - обработать изображение следующим образом для любой фотографии(цельный контур для каждой цифры и отсутствие посторонних контуров):

![alt text](https://github.com/komarov0512/seven-segment-digits-detection/blob/main/Image%20README/1.png)


### Программа:

![alt text](https://github.com/komarov0512/seven-segment-digits-detection/blob/main/Image%20README/2.png)
