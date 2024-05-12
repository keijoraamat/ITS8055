"""The starting point of the program"""
from Repository import Repository as Repo

Repo().interpolate_all_data()

data = Repo().get_interpolated_data('linear')
print(data[0])
