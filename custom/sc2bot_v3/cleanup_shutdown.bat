tskill tensorboard

del /q C:\dev\sc2ai\custom\sc2bot_v3\tensorboard\*
for /d %x in (C:\dev\sc2ai\custom\sc2bot_v3\tensorboard\*) do @rd /s /q "%x"

del /q C:\dev\sc2ai\custom\sc2bot_v3\brains\*
for /d %x in (C:\dev\sc2ai\custom\sc2bot_v3\brains\*) do @rd /s /q "%x"


