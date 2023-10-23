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
