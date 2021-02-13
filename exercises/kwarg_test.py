def print_kwargs(**kwargs):
    frida = None
    kunegonda = None
    for arg in kwargs:
        if arg == "frida":
            frida = kwargs[arg]
        if arg == "cunegonda":
            cunegonda = kwargs[arg]

    if None != frida:
        print(frida)
    if None != cunegonda:
        print(cunegonda)


lotus = "gugu"
nebrahim = "23m"

print_kwargs(frida = lotus, cunegonda = nebrahim)

#print_kwargs(lotus = gugu", frida = 2, nebrahim)
