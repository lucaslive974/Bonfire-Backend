with open("tests/linha_test.py", "r") as f:
    content = f.read()

# Fix insert_bulk
content = content.replace(
    "mock_db.query.return_value.filter.return_value.all.return_value = []",
    "mock_db.query.return_value.filter.return_value.all.side_effect = [[(107,), (108,)], []]",
)

# Fix insert_bulk_already_exists
content = content.replace(
    'mock_db.query.return_value.filter.return_value.all.return_value = [("61",)]',
    'mock_db.query.return_value.filter.return_value.all.side_effect = [[(107,)], [("61",)]]',
)

with open("tests/linha_test.py", "w") as f:
    f.write(content)
