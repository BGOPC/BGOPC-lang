from mainclasses.run import run

while True:
    text = input("Command !#> ")
    res, err = run('<stdin>', text)
    
    if err:
        print(err.as_string())
    else:
        print(res)
