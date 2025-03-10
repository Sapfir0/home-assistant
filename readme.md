# Home Assistant Configuration


## Common

| Device                          | Type |
| ------------------------------- | :--: |
| iPhone 15 Pro Max               |  🔍  |
| Garmin Fenix 7 Pro                  |  🔍  |
| Яндекс Алиса                    |  🔈  |
| Siri (only for ios automations) |  🔈  |


## Bed room

| Device                          | Type | Host |
| ------------------------------- | :--: | :--: |
| Xiaomi Mi Bed lamp 2            |💡| MiHome & HomeKit |

Самое сложное здесь - это добавить лампу во все приложения одновременно.
Путь должен быть примерно таким:

* Добавляем лампу в MiHome - оттуда будет брать устройства Яндекс.Дом
* Прокидываем bridge из HA в Homekit
* Из этого моста создаем девайс лампы в HA

На ночнике включается режим лампы-рассвета (wake_up_light.py), если input_boolean.wake_up_light выставляется в true.

__Расписание__

| Device     | Calculation  | Type |
| ------------| :--: | :--: |
| 09:15	| -15min |Включается лампа-рассвет |
| 09:30	| Base | Будильник, Отключатеся режим сна |
| 22:30:00 |  | Идет уход ко сну |

## Living room


| Device                  | Type | Host | Comment |
| ----------------------- | :--: | :--: | :--: |
| Xiaomi Mi Bulb 3x       |💡Light| MiHome | Создана группа "Люстра" в Яндексе
| QingPing Air Monitor    |🌡Climate| QingPing | Данные получаются через MQTT локально, экспортирована через YaHA Cloud
| Xiaomi TV Box 4k        |📺TV| HA |
| TP-Link TP110              |🎚 Smart plug| Tapo |
| Yandex Station Mini     |🔈Smart speaker & TTS | Yandex | Управляет домом из родного приложения

В комнате есть группа освещения, к которой применен adaptive lighting, (includes/adaptive_lighting)



## Hall


| Device                      | Type |
| --------------------------- | :--: |
| Raspberry Pi 4, 4GB RAM     |🖥|
| Beeling Mini S12 Pro N100, 16GB RAM  |🖥|
| Keenetic Giga               |🌎|

Здесь находится небольшая серверная, автоматизаций нет.

### Kitchen

| Device                          | Type | Host |
| ------------------------------- | :--: | :--: |
| Polaris PWK-1725CGLD | 🖥 | Polaris IQ HOME |


# Автоматизации



### Интеграция в Яндекс.Дом

[![FastPic.Ru](https://i122.fastpic.org/thumb/2023/1105/f8/1f73147a3b447009113a8e04ee9431f8.jpeg)](https://fastpic.org/view/122/2023/1105/1f73147a3b447009113a8e04ee9431f8.jpg.html)


Vactaion mode



* Когда прибываю домой -> выставляю переменную
* Когда ухожу тоже

https://disk.yandex.ru/d/_XcysP1cJYXF7w
