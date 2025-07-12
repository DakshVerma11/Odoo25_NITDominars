# Odoo25_NITDominars

**Submission for Odoo Hackathon 2025 by Team NITDominars**  
**Leader:** Daksh Verma  - verma11daksh@gmail.com
**Member:** Dheeraj Kumar - 231210039@nitdelhi.ac.in

---

## Problem Statement 2: StackIt – A Minimal Q&A Forum Platform

### Overview

**StackIt** is a minimal question-and-answer platform that supports collaborative learning and structured knowledge sharing. It’s designed to be simple, user-friendly, and focused on the core experience of asking and answering questions within a community.

 <img width="1893" height="871" alt="image" src="https://github.com/user-attachments/assets/47a30415-c731-4d03-b3fd-eb55e9589382" />

 <img width="1901" height="862" alt="image" src="https://github.com/user-attachments/assets/0074238e-91c7-461a-9441-650cf62fcbb3" />



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

  <img width="998" height="782" alt="image" src="https://github.com/user-attachments/assets/bb288f98-33a5-476c-aa50-20e2748ddbe4" />


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
 <img width="930" height="391" alt="image" src="https://github.com/user-attachments/assets/c0c05ab5-ef63-43cf-aed2-18d47c6b0fae" />


---

### 3. Answering Questions

- Users can post answers to any question  
- Answers can be formatted using the same rich text editor  
- Only logged-in users can post answers  

---

### 4. Voting & Accepting Answers

- Users can upvote or downvote answers  
- Question owners can mark one answer as accepted

  <img width="1471" height="309" alt="image" src="https://github.com/user-attachments/assets/3cc7bb0e-943c-4e15-9de0-5262612395ab" />


---

### 5. Tagging

- Questions must include relevant tags  
- Tags input supports multi-select (e.g., `React`, `JWT`)
  <img width="1591" height="611" alt="image" src="https://github.com/user-attachments/assets/f36c373e-503c-4ffc-8792-1a364fac71a9" />


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
