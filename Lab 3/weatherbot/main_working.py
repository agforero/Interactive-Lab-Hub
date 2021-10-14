from query import Query
from sys import argv


def correct(date):
    return "".join([c for c in date if c != "-"])


def main():
    Q = Query()
    
    with open("output.txt", 'w') as w:
        w.write(argv[1])
    
    Q.process_query(argv[1].split())


if __name__ == "__main__":
    main()
