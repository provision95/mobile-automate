import os

def main():
    if os.path.isdir('./Allure'):
        print('Allure directory exists!')
    else:
        os.mkdir('./Allure')
        print('Allure directory created!')

if __name__ == '__main__':
    main()