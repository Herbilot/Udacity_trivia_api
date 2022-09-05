
## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable 

### Endpoints 
#### GET /questions
- General:
    - Returns a list of category objects, question objects, success value, and total number of question
    - Results are paginated. each pages will display 10 questions. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
"categories": [
    {
      "id": 1, 
      "type": "Science"
    }, 
    {
      "id": 2, 
      "type": "Art"
    }, 
    {
      "id": 3, 
      "type": "Geography"
    }, 
    {
      "id": 4, 
      "type": "History"
    }, 
    {
      "id": 5, 
      "type": "Entertainment"
    }, 
    {
      "id": 6, 
      "type": "Sports"
    }
  ], 
  "questions": [
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 28, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 27, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 26, 
      "question": "What is my name?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 25, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 24, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 29, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 2, 
      "difficulty": 1, 
      "id": 33, 
      "question": "What is mye?"
    }
  ], 
  "success": true, 
  "total_questions": 26

```

#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created question, success value, total number of question, and a list of questions based on the page number. 
- `curl http://127.0.0.1:5000/questions?page=4 -X POST -H "Content-Type: application/json" -d '{"question":"do you like programming?", "answer":"Yes", "Category":"5", "difficulty":"1"}'`
```
new_question": 41, 
  "questions": [
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 38, 
      "question": "do you like programming?"
    }, 
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 39, 
      "question": "do you like programming?"
    }, 
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 40, 
      "question": "do you like programming?"
    }, 
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 41, 
      "question": "do you like programming?"
    }
  ], 
  "success": true, 
  "total_questions": 34
}

```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, a list of questions based on the page number and the total number of questions. 
- `curl -X DELETE http://127.0.0.1:5000/questions/41?page=4`
```
{
  "deleted_question": 41, 
  "questions": [
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 38, 
      "question": "do you like programming?"
    }, 
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 39, 
      "question": "do you like programming?"
    }, 
    {
      "answer": "Yes", 
      "category": null, 
      "difficulty": 1, 
      "id": 40, 
      "question": "do you like programming?"
    }
  ], 
  "success": true, 
  "total_questions": 33
}

```
#### GET /categories/1/questions
-General:
  -Returns a list of questions object based on category, succes value and the total number of questions that the category contains.
- Results are paginated. each pages will display 10 questions. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
{
  "category": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 24, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 25, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 26, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 27, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 28, 
      "question": "What is my name?"
    }, 
    {
      "answer": "Herbilot", 
      "category": 1, 
      "difficulty": 2, 
      "id": 29, 
      "question": "What is my name?"
    }
  ], 
  "success": true, 
  "total_questions": 9
}


```