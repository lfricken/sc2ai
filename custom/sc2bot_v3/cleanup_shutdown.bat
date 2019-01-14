del /q tensorboard\*
for /d %x in (tensorboard\*) do @rd /s /q "%x"

del /q brains\*
for /d %x in (brains\*) do @rd /s /q "%x"

tskill tensorboard
