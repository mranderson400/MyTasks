# TaskPal

**TaskPal** is an intelligent task management system designed to simplify your workflow. By integrating a chatbot interface, it allows you to create, manage, and view tasks effortlessly. With a user-friendly dashboard, TaskPal makes it easy to keep track of your tasks and stay organized.

---

## Features

- **Chatbot Task Creation**: Use a chatbot interface to quickly create tasks by simply providing a description.
- **Task Overview**: View all tasks with details such as title, description, due date, status, and actions (edit, delete).
- **Task Status**: Tasks come with status labels such as "Pending", "In Progress", and "Completed".
- **User Authentication**: Log in to access your personal task list and manage your tasks.
- **Responsive Design**: Fully responsive interface to work across desktop and mobile devices.
- **Seamless Integration**: Easily create tasks from the chatbot and have them instantly available in your task list.

---

## Tech Stack

- **Frontend**: HTML, Bootstrap 5, jQuery
- **Backend**: FastAPI, Python
- **Database**: MongoDB
- **NLP**: spaCy for date extraction in task descriptions

---

## Installation

### Prerequisites

Before you can run TaskPal, ensure you have the following installed:

- Python 3.8 or higher
- MongoDB instance

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/BHI-110065/TaskPal.git
   cd TaskPal
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install the spacy `en_core_web_sm` dataset:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. Run the FastAPI server:
   ```bash
   uvicorn server:app --reload
   ```

---

## Usage

1. **Creating a Task**:
   - You can use the chatbot interface to describe a task and create it. The system automatically extracts the task details like due date and assigns it a random status.
   
2. **Viewing Tasks**:
   - Once created, tasks will appear on the dashboard with all details, such as title, description, due date, and status.

3. **Task Actions**:
   - You can edit or delete tasks that you have created.
   - The status of tasks can be updated as well.

---

## Contributing

We welcome contributions to **TaskPal**. If you want to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new Pull Request.

---


## Acknowledgments

- **spaCy** for natural language processing to extract dates from task descriptions.
- **FastAPI** for building the backend API quickly and efficiently.
- **Bootstrap** for creating a responsive and visually appealing UI.

---
