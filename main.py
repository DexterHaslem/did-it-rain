APIKEYFILE = 'darksky.key'


def get_api_key():
    with open(APIKEYFILE) as f:
        l = f.readline()
        return l.strip()


def main():
    print get_api_key()


if __name__ == "__main__":
    main()
