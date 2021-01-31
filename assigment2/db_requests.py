UPDATE = """UPDATE posts INNER JOIN users ON users.userId = users.userId  
            SET uniqueId = :unique_id, postUrl= :post_url, username= :usernames, 
            userKarma= :user_karma, userCakeDay=:user_CakeDay, 
            postKarma = :post_karma, commentKarma=:comment_karma,
            postDate= :post_date, numberOfComments =:number_OfComments,
            numberOfVotes =:number_OfVotes, postCategory =:post_Category WHERE uniqueId =:uniqueId"""
GET_DATA = "SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId"
GET_POST = "SELECT * FROM posts LEFT JOIN users ON posts.userId=users.userId WHERE uniqueId= :uniqueId"
DELETE = "DELETE FROM posts USING users WHERE posts.userID=users.userId AND uniqueId= :uniqueId"
