from query import Query
from sys import argv


def correct(date):
    return "".join([c for c in date if c != "-"])


def main():
    Q = Query()
    Q.process_query(argv[1:])


if __name__ == "__main__":
    main()
