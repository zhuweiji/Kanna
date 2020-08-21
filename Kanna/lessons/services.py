from .models import Script

with open("matthew.txt", "r+") as f:
    text = f.read()


script = Script.objects.get(pk=7)
print(script.flags)