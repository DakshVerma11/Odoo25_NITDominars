-- Seed data for StackIt Q&A Platform

-- Admin User
INSERT INTO users (username, email, password_hash, role) 
VALUES ('admin', 'admin@stackit.com', '$2b$12$1jsTJ0tZ1BKRCpKWWQEJKOwG0YbZ1uEEcIFbQlNbESLODHXnjaB1i', 'admin');

-- Regular Users
INSERT INTO users (username, email, password_hash) 
VALUES ('johndoe', 'john@example.com', '$2b$12$QJA/VWWtm.QC9ujYLMZzQO94M0DalVVpD5DTiKE5NNslGUrIgQ2S6');

INSERT INTO users (username, email, password_hash) 
VALUES ('janedoe', 'jane@example.com', '$2b$12$QJA/VWWtm.QC9ujYLMZzQO94M0DalVVpD5DTiKE5NNslGUrIgQ2S6');

INSERT INTO users (username, email, password_hash) 
VALUES ('bobsmith', 'bob@example.com', '$2b$12$QJA/VWWtm.QC9ujYLMZzQO94M0DalVVpD5DTiKE5NNslGUrIgQ2S6');

-- Tags
INSERT INTO tags (name) VALUES ('javascript');
INSERT INTO tags (name) VALUES ('python');
INSERT INTO tags (name) VALUES ('react');
INSERT INTO tags (name) VALUES ('flask');
INSERT INTO tags (name) VALUES ('node.js');
INSERT INTO tags (name) VALUES ('html');
INSERT INTO tags (name) VALUES ('css');
INSERT INTO tags (name) VALUES ('database');
INSERT INTO tags (name) VALUES ('api');
INSERT INTO tags (name) VALUES ('security');

-- Questions
INSERT INTO questions (user_id, title, description)
VALUES (
    2, 
    'How to use React hooks effectively?', 
    '<p>I\'m new to React hooks and I\'m trying to understand how to use them effectively. Specifically, I\'m confused about the dependency array in useEffect.</p><p>For example, what\'s the difference between these two implementations?</p><pre><code>useEffect(() => { /* do something */ }, []);\nuseEffect(() => { /* do something */ }, [someValue]);</code></pre><p>When should I use an empty dependency array versus including values?</p>'
);

INSERT INTO questions (user_id, title, description)
VALUES (
    3, 
    'Best practices for securing a Flask API', 
    '<p>I\'m building a RESTful API with Flask and I want to make sure it\'s secure. What are some best practices I should follow?</p><p>Specifically:</p><ul><li>What\'s the best way to handle authentication?</li><li>How should I protect against CSRF attacks?</li><li>How can I prevent SQL injection?</li></ul><p>Any other security tips would be appreciated!</p>'
);

INSERT INTO questions (user_id, title, description)
VALUES (
    4, 
    'Optimizing database queries for large datasets', 
    '<p>I\'m working with a database that has grown quite large (millions of records) and my queries are starting to slow down.</p><p>What strategies can I use to optimize these queries? I\'m using MySQL but general advice is welcome too.</p><p>Here\'s an example of a query that\'s performing poorly:</p><pre><code>SELECT u.*, COUNT(o.id) as order_count\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id\nWHERE u.status = \'active\'\nGROUP BY u.id\nORDER BY order_count DESC;</code></pre>'
);

-- Connect questions to tags
INSERT INTO question_tags (question_id, tag_id) VALUES (1, 3); -- React
INSERT INTO question_tags (question_id, tag_id) VALUES (1, 1); -- JavaScript

INSERT INTO question_tags (question_id, tag_id) VALUES (2, 4); -- Flask
INSERT INTO question_tags (question_id, tag_id) VALUES (2, 10); -- Security
INSERT INTO question_tags (question_id, tag_id) VALUES (2, 9); -- API

INSERT INTO question_tags (question_id, tag_id) VALUES (3, 8); -- Database

-- Answers
INSERT INTO answers (question_id, user_id, content)
VALUES (
    1, 
    4, 
    '<p>The dependency array in <code>useEffect</code> determines when the effect should run:</p><ul><li><strong>Empty array <code>[]</code></strong>: The effect runs only once after the initial render, similar to <code>componentDidMount</code> in class components.</li><li><strong>With dependencies <code>[someValue]</code></strong>: The effect runs after the initial render and whenever any of the dependencies change.</li><li><strong>No dependency array</strong>: The effect runs after every render.</li></ul><p>Use an empty array when your effect doesn\'t depend on any values from props or state and only needs to run once. For example, when fetching initial data or setting up subscriptions.</p><p>Include dependencies when your effect uses values from props or state that could change. React will re-run the effect when those values change.</p><p>A common mistake is forgetting to include all the dependencies that your effect uses, which can lead to stale closures and bugs.</p>'
);

INSERT INTO answers (question_id, user_id, content, accepted)
VALUES (
    2, 
    2, 
    '<p>Here are some best practices for securing a Flask API:</p><h3>Authentication</h3><ul><li>Use JWT (JSON Web Tokens) for stateless authentication</li><li>Implement proper password hashing with bcrypt or Argon2</li><li>Set proper expiration times for tokens</li><li>Use refresh tokens for long-lived sessions</li></ul><h3>CSRF Protection</h3><p>For API endpoints that use cookies for authentication, use Flask-WTF\'s CSRF protection. For token-based auth (JWT), CSRF is generally not a concern.</p><h3>SQL Injection Prevention</h3><ul><li>Use SQLAlchemy ORM which handles parameterization</li><li>If writing raw SQL, always use parameterized queries</li><li>Never concatenate user input into SQL strings</li></ul><h3>Additional Security Measures</h3><ul><li>Use HTTPS in production</li><li>Implement rate limiting to prevent brute force attacks</li><li>Add proper input validation for all API endpoints</li><li>Set secure headers (X-Content-Type-Options, X-Frame-Options, etc.)</li><li>Implement proper error handling that doesn\'t leak sensitive information</li></ul>',
    TRUE
);

INSERT INTO answers (question_id, user_id, content)
VALUES (
    3, 
    3, 
    '<p>For optimizing queries on large datasets, here are some strategies:</p><h3>1. Index your columns properly</h3><p>Make sure you have indexes on columns used in WHERE, JOIN, ORDER BY, and GROUP BY clauses. For your example:</p><pre><code>CREATE INDEX idx_user_status ON users(status);\nCREATE INDEX idx_orders_user_id ON orders(user_id);</code></pre><h3>2. Rewrite the query</h3><p>For count operations, consider using subqueries:</p><pre><code>SELECT u.*, o.order_count\nFROM users u\nLEFT JOIN (\n    SELECT user_id, COUNT(*) as order_count\n    FROM orders\n    GROUP BY user_id\n) o ON u.id = o.user_id\nWHERE u.status = \'active\'\nORDER BY o.order_count DESC;</code></pre><h3>3. Pagination</h3><p>Don\'t fetch all records at once. Use LIMIT and OFFSET to paginate results.</p><h3>4. Consider denormalization</h3><p>For frequently accessed counts, consider storing the count in the users table and updating it when orders change.</p><h3>5. Database-specific optimizations</h3><p>For MySQL specifically:<ul><li>Use EXPLAIN to analyze your queries</li><li>Consider table partitioning for very large tables</li><li>Optimize your server configuration (buffer sizes, etc.)</li></ul></p>'
);

-- Comments
INSERT INTO comments (answer_id, user_id, content)
VALUES (1, 3, 'Great explanation! I would add that React\'s exhaustive-deps ESLint rule can help identify missing dependencies.');

INSERT INTO comments (answer_id, user_id, content)
VALUES (2, 4, 'I\'ve been using Flask-JWT-Extended for authentication and it works really well.');

INSERT INTO comments (answer_id, user_id, content)
VALUES (3, 2, 'Denormalization has worked well for us too. We have a counter table for frequently accessed metrics.');

-- Votes
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (1, 2, 'up');
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (1, 3, 'up');
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (2, 3, 'up');
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (2, 4, 'up');
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (3, 2, 'up');
INSERT INTO votes (answer_id, user_id, vote_type) VALUES (3, 4, 'down');

-- Notifications
INSERT INTO notifications (user_id, type, source_id, read)
VALUES (2, 'answer', 1, 0);

INSERT INTO notifications (user_id, type, source_id, read)
VALUES (3, 'comment', 2, 0);

INSERT INTO notifications (user_id, type, source_id, read)
VALUES (4, 'mention', 3, 1);