use posts
db.createCollection("posts", {'capped': true, max: 1000})
