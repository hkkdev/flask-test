from app import *

u = models.User(username = 'aaa', 
                email = 'aaa', 
                password = 'aaa')
db.session.add(u)

p = models.Posts(content = 'This is my first post',
                 author = u)
db.session.add(p)

c = models.Comments(comment = 'FIRST comment ever',
                    post = p,
                    author = u)
db.session.add(c)


db.session.commit()


