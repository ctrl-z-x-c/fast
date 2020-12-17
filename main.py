# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from gia_report import gia
from fastapi import FastAPI

app = FastAPI()

app.include_router(gia.Gia_Router, prefix='/user')

if __name__ == '__main__':
    pass
