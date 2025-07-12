# Odoo25_NITDominars

**Submission for Odoo Hackathon 2025 by Team NITDominars**  
**Leader:** Daksh Verma  - verma11daksh@gmail.com
**Member:** Dheeraj Kumar - 231210039@nitdelhi.ac.in

---

## Problem Statement 2: StackIt – A Minimal Q&A Forum Platform

### Overview

**StackIt** is a minimal question-and-answer platform that supports collaborative learning and structured knowledge sharing. It’s designed to be simple, user-friendly, and focused on the core experience of asking and answering questions within a community.

---

## User Roles

| Role  | Permissions                                          |
|-------|------------------------------------------------------|
| Guest | View all questions and answers                       |
| User  | Register, log in, post questions/answers, vote       |
| Admin | Moderate content                                     |

---

## Core Features (Must-Have)

### 1. Ask Question

Users can submit a new question using:
- **Title** – Short and descriptive
- **Description** – Written using a rich text editor

---

### Admin Role

- Reject inappropriate or spammy skill descriptions  
- Ban users who violate platform policies  
- Monitor pending, accepted, or cancelled swaps  
- Send platform-wide messages (e.g., feature updates, downtime alerts)  
- Download reports of user activity, feedback logs, and swap stats  

**Mockup:** [View Mockup](https://link.excalidraw.com/l/65VNwvy7c4X/8bM86GXnnUN)

---

### 2. Rich Text Editor Features

The description editor should support:

- **Bold**, *Italic*, ~~Strikethrough~~  
- Numbered lists, bullet points  
- Emoji insertion 😊  
- Hyperlink insertion (URLs)  
- Image upload  
- Text alignment – Left, Center, Right  

---

### 3. Answering Questions

- Users can post answers to any question  
- Answers can be formatted using the same rich text editor  
- Only logged-in users can post answers  

---

### 4. Voting & Accepting Answers

- Users can upvote or downvote answers  
- Question owners can mark one answer as accepted  

---

### 5. Tagging

- Questions must include relevant tags  
- Tags input supports multi-select (e.g., `React`, `JWT`)  

---

### 6. Notification System

- A notification icon (bell) appears in the top navigation bar  
- Users are notified when:
  - Someone answers their question  
  - Someone comments on their answer  
  - Someone mentions them using `@username`  
- The icon shows the number of unread notifications  
- Clicking the icon opens a dropdown with recent notifications  

**Mockup:** [View Notification Mockup](https://link.excalidraw.com/l/65VNwvy7c4X/9mhEahV0MQg)
