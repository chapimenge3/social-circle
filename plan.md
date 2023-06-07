# Social Circle App Plan

## Database Design

### Users

| Column Name     | Data Type | Details                   |
| --------------- | --------- | ------------------------- |
| id              | integer   | not null, primary key     |
| username        | string    | not null, indexed, unique |
| email           | string    | not null, indexed, unique |
| password_digest | string    | not null                  |
| session_token   | string    | not null, indexed, unique |
| profile_pic_url | string    |                           |
| bio             | text      |                           |
| birth_date      | datetime  |                           |
| location        | string    |                           |
| is_admin        | boolean   | not null, default: false  |
| created_at      | datetime  | not null                  |
| updated_at      | datetime  | not null                  |

### Friends

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| user_id     | integer   | not null, foreign key (references users), indexed |
| friend_id   | integer   | not null, foreign key (references users), indexed |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Friend Requests

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| sender_id   | integer   | not null, foreign key (references users), indexed |
| receiver_id | integer   | not null, foreign key (references users), indexed |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Posts

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| author_id   | integer   | not null, foreign key (references users), indexed |
| body        | text      | not null                                          |
| image       | string    |                                                   |
| video       | string    |                                                   |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Comments

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| author_id   | integer   | not null, foreign key (references users), indexed |
| post_id     | integer   | not null, foreign key (references posts), indexed |
| body        | text      | not null                                          |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Likes

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| liker_id    | integer   | not null, foreign key (references users), indexed |
| post_id     | integer   | not null, foreign key (references posts), indexed |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Messages

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| sender_id   | integer   | not null, foreign key (references users), indexed |
| receiver_id | integer   | not null, foreign key (references users), indexed |
| body        | text      | not null                                          |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

### Notifications

| Column Name | Data Type | Details                                           |
| ----------- | --------- | ------------------------------------------------- |
| id          | integer   | not null, primary key                             |
| user_id     | integer   | not null, foreign key (references users), indexed |
| body        | text      | not null                                          |
| created_at  | datetime  | not null                                          |
| updated_at  | datetime  | not null                                          |

## Features

Django Apps:

1 Accounts

- Handles user authentication, registration, and account management.
- Includes views for user login, registration, profile settings, and password reset.

2 Profiles

- Manages user profiles and profile-related functionality.
- Allows users to view and edit their profiles, including bio, profile image, and additional information.

3 Posts

- Handles creating, viewing, and managing posts.
- Includes functionalities like creating a new post, displaying posts in the feed, and enabling users to like and comment on posts.

4 Comments

- Manages comments on posts.
- Provides functionalities for adding comments to posts, displaying comments, and allowing users to reply to comments.

5 Likes

- Handles the liking functionality for posts.
- Enables users to like or unlike posts and keeps track of the number of likes for each post.

6 Friends

- Manages friend requests and user connections.
- Allows users to send and accept friend requests, view their friend list, and handle friend-related actions.

7 Messages

- Handles private messaging between users.
- Provides functionalities for sending and receiving messages, displaying message history, and managing conversations.

8 Notifications

- Manages user notifications for various activities.
- Sends notifications to users for actions like new friend requests, new messages, post likes, and comments.

9 Search

- Implements search functionality across users, posts, and other users, posts other relevant entities.
- Allows users to search for other users, posts, or specific content within the social media platform.

10 Settings

- Manages application settings and configurations.
- Includes functionalities like managing email preferences, privacy settings, and account security settings.
