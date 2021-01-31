UPDATE = """UPDATE posts INNER JOIN users ON users.userId = users.userId  
            SET uniqueId = :unique_id, postUrl= :post_url, username= :usernames, 
            userKarma= :user_karma, userCakeDay=:user_CakeDay, 
            postKarma = :post_karma, commentKarma=:comment_karma,
            postDate= :post_date, numberOfComments =:number_OfComments,
            numberOfVotes =:number_OfVotes, postCategory =:post_Category WHERE uniqueId =:uniqueId"""
GET_DATA = "SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId"
GET_POST = "SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId WHERE uniqueId= %s"
DELETE = "DELETE FROM posts USING users WHERE posts.userID=users.userId AND uniqueId= :uniqueId"
INSERT_POST = """INSERT INTO posts (uniqueId,postUrl,postKarma,commentKarma,postDate,numberOfComments,numberOfvotes,
              postCategory,userId) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
INSERT_USER = 'INSERT INTO users (username,userKarma,userCakeDay) VALUES (%s,%s,%s) RETURNING users.userId'
