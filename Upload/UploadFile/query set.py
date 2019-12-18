from pypika import Query, Table, Field

q = Query.from_('Upload').select('id', 'Phone Number', 'Student Name','DateOfDrive')
print(str(q))