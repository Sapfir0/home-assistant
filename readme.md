# Home Assistant Configuration

## Hardware

| Device                          | Type |
| ------------------------------- | :--: |
| Xiaomi Mi Bed lamp 2            |  💡  |
| Xiaomi Mi Bulb                  |  💡  |
| QingPing Air Monitor            |  🌡   |
| Raspberry Pi 4, 4GB RAM         |  🖥   |
| Polaris PWK-1725CGLD            |  🖥   |
| Dreame L10 Ultra                |  🖥   |
| D-Link DIR-615                  |  🎚   |
| iPhone 13                       |  🔍  |
| Apple Watch SE                  |  🔍  |
| Яндекс Алиса                    |  🔈  |
| Siri (only for ios automations) |  🔈  |

## Automation & logic

Освещение

В комнате есть группа освещения, к которой применен adaptive lighting, (includes/adaptive_lighting)

В спальне есть лампа, у нее есть (wake_up_light.py), если input_boolean.wake_up_light выставляется в true

Vactaion mode


Автоматизации из shortcuts:

* При выключении будильника -> выключается ночник
* Когда происходит waking up -> выключаем sleep mode в ha, (также выключаем disturb mode в ios)
* Когда прибываю домой -> выставляю переменную
* Когда ухожу тоже


Расписание

| Device     | Calculation  | Type |
| ------------| :--: | :--: |
| 08:00 | -1hour	| Включается розетка для зарядки всякого разного |
| 08:45	| -15min |Включается лампа-рассвет |
| 09:00	| Base | Будильник, Отключатеся режим сна |
| 09:01	| +1min | Отправляется уведомление о погоде |
| 22:30:00 |  | Идет уход ко сну |
| 00:04  | | Синхронизация будильников |