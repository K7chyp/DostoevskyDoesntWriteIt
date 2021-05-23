from pageparser import GetBookText
from csv import writer

FILENAME: str = str(input("Input file name "))
with open("{}.csv".format(FILENAME), "w") as file_:
    write_ = writer(file_)
    write_.writerow(["book_name", "text"])
    for href, text in GetBookText("/books/idiot").book_content.items():
        write_.writerow([href, text])
