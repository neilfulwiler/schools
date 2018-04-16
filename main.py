import requests


GREATSCHOOLS_URL = 'https://www.greatschools.org/'



def main():
    result = requests.get(GREATSCHOOLS_URL).json
    print(result)



if __name__ == '__main__':
    main()
