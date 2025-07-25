# 112 Odin Integration for Home Assistant

Fetches emergency data from ODIN RSS feeds.

## Configuration
```yaml
sensor:
  - platform: 112odin
    name: 112 ODIN
    beredskabsID: "123"
    stations_navn: "Station Nord"
    antal_haendelser: 10
```