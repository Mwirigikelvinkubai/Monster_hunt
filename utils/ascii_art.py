#	Store banner art & monster sprites for nicer CLI output
ART = {
    "logo":
r"""xxxxxxxx
"""
}
def show(name):
    print(ART.get(name, ""))
