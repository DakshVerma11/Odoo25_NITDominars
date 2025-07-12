-- Performance indexes for StackIt Q&A Platform

-- Users table indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Questions table indexes
CREATE INDEX idx_questions_user_id ON questions(user_id);
CREATE INDEX idx_questions_created_at ON questions(created_at);
CREATE INDEX idx_questions_title ON questions(title);

-- Answers table indexes
CREATE INDEX idx_answers_question_id ON answers(question_id);
CREATE INDEX idx_answers_user_id ON answers(user_id);
CREATE INDEX idx_answers_created_at ON answers(created_at);
CREATE INDEX idx_answers_accepted ON answers(accepted);

-- Tags table index (name is already unique)
-- No additional indexes needed

-- Question Tags table indexes
-- The primary key already includes both columns, no additional indexes needed

-- Votes table indexes
CREATE INDEX idx_votes_answer_id ON votes(answer_id);
CREATE INDEX idx_votes_user_id ON votes(user_id);
CREATE INDEX idx_votes_type ON votes(vote_type);

-- Comments table indexes
CREATE INDEX idx_comments_answer_id ON comments(answer_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);
CREATE INDEX idx_comments_created_at ON comments(created_at);

-- Notifications table indexes
CREATE INDEX idx_notifications_user_id ON notifications(user_id);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, read);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);

-- Full-text search indexes for MySQL
-- Uncomment for MySQL databases
-- CREATE FULLTEXT INDEX idx_questions_fulltext ON questions(title, description);

-- Composite indexes for common query patterns
CREATE INDEX idx_questions_user_created ON questions(user_id, created_at);
CREATE INDEX idx_answers_question_created ON answers(question_id, created_at);
CREATE INDEX idx_notifications_user_created ON notifications(user_id, created_at);