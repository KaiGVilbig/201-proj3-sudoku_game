def main():

    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    b = list(a)
    
    b[0] = 2

    print(a)

    a[0] = 12

    print(b)

main()
